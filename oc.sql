USE [365DB]
GO
/****** Object:  Trigger [dbo].[OCControl]    Script Date: 29/03/2016 20:47:53 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

ALTER TRIGGER [dbo].[OCControl]
ON [dbo].[t365_HorarioControl]
FOR INSERT
AS
     DECLARE @idcliente int
     DECLARE @dayweek int
     DECLARE @cod_alarm nvarchar(3)
     DECLARE @minapertura time
     DECLARE @maxapertura time
     DECLARE @mincierre time
     DECLARE @maxcierre time
     DECLARE @fechaevento datetime
     DECLARE @idprotocolo int

     SET @dayweek = DATEPART(dw, GETDATE())

     SELECT
          @idcliente = id_cliente,
          @cod_alarm = cod_alarm,
          @fechaevento = fecha
     FROM inserted

     IF @dayweek = DATEPART(WEEKDAY, @fechaevento)
     BEGIN
          IF @cod_alarm = 'APE'
          BEGIN
               SELECT
                    @minapertura = DATEADD(mi, -
                    t365_horariosoc.toleranciaapertura,
                    t365_horariosoc.horaapertura),
                    @maxapertura =
                    DATEADD(mi, t365_horariosoc.toleranciaapertura,
                    t365_horariosoc.horaapertura),
                    @idprotocolo = t365_clientes.id_protocolo
               FROM t365_horariosoc
               INNER JOIN t365_clientes
                    ON t365_horariosoc.id_cliente =
                    t365_clientes.id_cliente
               WHERE (DATEADD(mi, t365_horariosoc.toleranciacierre,
               t365_horariosoc.horacierre) >=
               CAST(GETDATE() AS time)
               OR DATEADD(mi, -t365_horariosoc.toleranciaapertura,
               t365_horariosoc.horaapertura)
               >= CAST(GETDATE() AS time)
               OR DATEADD(mi, -t365_horariosoc.toleranciaapertura,
               t365_horariosoc.horaapertura) <
               CAST(GETDATE() AS time)
               AND DATEADD(mi, t365_horariosoc.toleranciacierre,
               t365_horariosoc.horacierre) <
               DATEADD(mi, -
               t365_horariosoc.toleranciaapertura,
               t365_horariosoc.horaapertura))
               AND (t365_horariosoc.diaapertura = @dayweek)
               AND t365_horariosoc.id_cliente = @idcliente
               ORDER BY t365_horariosoc.horaapertura DESC

               IF @@ROWCOUNT > 0
               BEGIN
                    IF @minapertura < CONVERT(time, @fechaevento)
                         AND @maxapertura > CONVERT(time, @fechaevento)
                    BEGIN
                         PRINT 'Apertura dentro de horario establecido'
                    END
                    ELSE
                    BEGIN
                         IF @minapertura > CONVERT(time, @fechaevento)
                         BEGIN
                              PRINT 'Apertura Temprana'

                              EXEC Jssp_insertartramasistema 'Evento Horario',
                                                             @idcliente,
                                                             'E365_APETEMP',
                                                             '',
                                                             @idprotocolo,
                                                             @fechaevento,
                                                             ' ',
                                                             '1',
                                                             '100'
                         END
                         ELSE
                         BEGIN
                              PRINT 'Apertura Tarde'

                              EXEC Jssp_insertartramasistema 'Evento Horario',
                                                             @idcliente,
                                                             'E365_APETARD',
                                                             '',
                                                             @idprotocolo,
                                                             @fechaevento,
                                                             ' ',
                                                             '1',
                                                             '100'
                         END
                    END
               END
               ELSE
               BEGIN
                    SELECT
                         @idprotocolo = id_protocolo
                    FROM t365_clientes
                    WHERE id_cliente = @idcliente

                    PRINT 'Apertura Fuera de Horario'

                    EXEC Jssp_insertartramasistema 'Evento Horario',
                                                   @idcliente,
                                                   'E365_APEFHOR',
                                                   '',
                                                   @idprotocolo,
                                                   @fechaevento,
                                                   ' ',
                                                   '1',
                                                   '100'
               END
          END
          ELSE
          BEGIN
               SELECT
                    @mincierre = DATEADD(mi, -
                    t365_horariosoc.toleranciacierre,
                    t365_horariosoc.horacierre),
                    @maxcierre = DATEADD(mi,
                    t365_horariosoc.toleranciacierre,
                    t365_horariosoc.horacierre),
                    @idprotocolo = t365_clientes.id_protocolo
               FROM t365_horariosoc
               INNER JOIN t365_clientes
                    ON t365_horariosoc.id_cliente =
                    t365_clientes.id_cliente
               WHERE (DATEADD(mi, t365_horariosoc.toleranciacierre,
               t365_horariosoc.horacierre) >=
               CAST(GETDATE() AS time)
               OR DATEADD(mi, -t365_horariosoc.toleranciaapertura,
               t365_horariosoc.horaapertura)
               >= CAST(GETDATE() AS time)
               OR DATEADD(mi, -t365_horariosoc.toleranciaapertura,
               t365_horariosoc.horaapertura) <
               CAST(GETDATE() AS time)
               AND DATEADD(mi, t365_horariosoc.toleranciacierre,
               t365_horariosoc.horacierre) <
               DATEADD(mi, -
               t365_horariosoc.toleranciaapertura,
               t365_horariosoc.horaapertura))
               AND (t365_horariosoc.diacierre = @dayweek)
               AND t365_horariosoc.id_cliente = @idcliente
               ORDER BY t365_horariosoc.horacierre ASC

               IF @@ROWCOUNT > 0
               BEGIN
                    IF @mincierre < CONVERT(time, @fechaevento)
                         AND @maxcierre > CONVERT(time, @fechaevento)
                    BEGIN
                         PRINT 'Cierre dentro de horario establecido'
                    END
                    ELSE
                    BEGIN
                         IF @mincierre > CONVERT(time, @fechaevento)
                         BEGIN
                              PRINT 'Cierre Temprano'

                              EXEC Jssp_insertartramasistema 'Evento Horario',
                                                             @idcliente,
                                                             'E365_CIETEMP',
                                                             '',
                                                             @idprotocolo,
                                                             @fechaevento,
                                                             ' ',
                                                             '1',
                                                             '100'
                         END
                         ELSE
                         BEGIN
                              PRINT 'Cierre Tarde'

                              EXEC Jssp_insertartramasistema 'Evento Horario',
                                                             @idcliente,
                                                             'E365_CIETARD',
                                                             '',
                                                             @idprotocolo,
                                                             @fechaevento,
                                                             ' ',
                                                             '1',
                                                             '100'
                         END
                    END
               END
               ELSE
                    SELECT
                         @mincierre = DATEADD(mi, -
                         t365_horariosoc.toleranciacierre,
                         t365_horariosoc.horacierre),
                         @maxcierre = DATEADD(mi,
                         t365_horariosoc.toleranciacierre,
                         t365_horariosoc.horacierre),
                         @idprotocolo = t365_clientes.id_protocolo
                    FROM t365_horariosoc
                    INNER JOIN t365_clientes
                         ON t365_horariosoc.id_cliente =
                         t365_clientes.id_cliente
                    WHERE (t365_horariosoc.diacierre = @dayweek)
                    AND t365_horariosoc.id_cliente = @idcliente
                    ORDER BY t365_horariosoc.horacierre DESC
               IF @@ROWCOUNT > 0
               BEGIN
                    PRINT 'Cierre Tarde2'

                    EXEC Jssp_insertartramasistema 'Evento Horario',
                                                   @idcliente,
                                                   'E365_CIETARD',
                                                   '',
                                                   @idprotocolo,
                                                   @fechaevento,
                                                   ' ',
                                                   '1',
                                                   '100'
               END
               ELSE
               BEGIN
                    SELECT
                         @idprotocolo = id_protocolo
                    FROM t365_clientes
                    WHERE id_cliente = @idcliente

                    PRINT 'Cierre Fuera de Horario'

                    EXEC Jssp_insertartramasistema 'Evento Horario',
                                                   @idcliente,
                                                   'E365_CIEFHOR',
                                                   '',
                                                   @idprotocolo,
                                                   @fechaevento,
                                                   ' ',
                                                   '1',
                                                   '100'
               END
          END
     END