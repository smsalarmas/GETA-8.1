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
    DECLARE @idcliente INT 
    DECLARE @dayweek INT 
    DECLARE @cod_alarm NVARCHAR(3) 
    DECLARE @minapertura TIME 
    DECLARE @maxapertura TIME 
    DECLARE @mincierre TIME 
    DECLARE @maxcierre TIME 
    DECLARE @fechaevento DATETIME 
    DECLARE @idprotocolo INT 

    SET @dayweek = Datepart(dw, Getdate()) 

    SELECT @idcliente = id_cliente, 
           @cod_alarm = cod_alarm, 
           @fechaevento = fecha 
    FROM   inserted 

    IF @dayweek = Datepart(weekday, @fechaevento) 
      BEGIN 
          IF @cod_alarm = 'APE' 
            BEGIN 
                SELECT @minapertura = Dateadd(mi, - 
                                      t365_horariosoc.toleranciaapertura, 
                                             t365_horariosoc.horaapertura), 
                       @maxapertura = 
                       Dateadd(mi, t365_horariosoc.toleranciaapertura, 
                       t365_horariosoc.horaapertura), 
                       @idprotocolo = t365_clientes.id_protocolo 
                FROM   t365_horariosoc 
                       INNER JOIN t365_clientes 
                               ON t365_horariosoc.id_cliente = 
                                  t365_clientes.id_cliente 
                WHERE  ( Dateadd(mi, t365_horariosoc.toleranciacierre, 
                         t365_horariosoc.horacierre) >= 
                                  Cast(Getdate() AS TIME) 
                          OR Dateadd(mi, -t365_horariosoc.toleranciaapertura, 
                             t365_horariosoc.horaapertura) 
                             >= Cast(Getdate() AS TIME) 
                          OR Dateadd(mi, -t365_horariosoc.toleranciaapertura, 
                             t365_horariosoc.horaapertura) < 
                                 Cast(Getdate() AS TIME) 
                             AND Dateadd(mi, t365_horariosoc.toleranciacierre, 
                                 t365_horariosoc.horacierre) < 
                                 Dateadd(mi, - 
t365_horariosoc.toleranciaapertura, 
                                 t365_horariosoc.horaapertura) ) 
                       AND ( t365_horariosoc.diaapertura = @dayweek ) 
                       AND t365_horariosoc.id_cliente = @idcliente 
                ORDER  BY t365_horariosoc.horaapertura DESC 

                IF @@ROWCOUNT > 0 
                  BEGIN 
                      IF @minapertura < CONVERT(TIME, @fechaevento) 
                         AND @maxapertura > CONVERT(TIME, @fechaevento)
             BEGIN
                        PRINT 'Apertura dentro de horario establecido' 
             END
                      ELSE 
                        BEGIN 
                            IF @minapertura > CONVERT(TIME, @fechaevento) 
                              BEGIN 
                                  PRINT 'Apertura Temprana' 

                                  EXEC Jssp_insertartramasistema 
                                    'Evento Horario', 
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

                                  EXEC Jssp_insertartramasistema 
                                    'Evento Horario', 
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
                      SELECT @idprotocolo = id_protocolo 
                      FROM   t365_clientes 
                      WHERE  id_cliente = @idcliente 

                      PRINT 'Apertura Fuera de Horario' 

                      EXEC Jssp_insertartramasistema 
                        'Evento Horario', 
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
                SELECT @mincierre = Dateadd(mi, - 
                                    t365_horariosoc.toleranciacierre, 
                                           t365_horariosoc.horacierre), 
                       @maxcierre = Dateadd(mi, 
t365_horariosoc.toleranciacierre, 
                                    t365_horariosoc.horacierre), 
                       @idprotocolo = t365_clientes.id_protocolo 
                FROM   t365_horariosoc 
                       INNER JOIN t365_clientes 
                               ON t365_horariosoc.id_cliente = 
                                  t365_clientes.id_cliente 
                WHERE  ( Dateadd(mi, t365_horariosoc.toleranciacierre, 
                         t365_horariosoc.horacierre) >= 
                                  Cast(Getdate() AS TIME) 
                          OR Dateadd(mi, -t365_horariosoc.toleranciaapertura, 
                             t365_horariosoc.horaapertura) 
                             >= Cast(Getdate() AS TIME) 
                          OR Dateadd(mi, -t365_horariosoc.toleranciaapertura, 
                             t365_horariosoc.horaapertura) < 
                                 Cast(Getdate() AS TIME) 
                             AND Dateadd(mi, t365_horariosoc.toleranciacierre, 
                                 t365_horariosoc.horacierre) < 
                                 Dateadd(mi, - 
t365_horariosoc.toleranciaapertura, 
                                 t365_horariosoc.horaapertura) ) 
                       AND ( t365_horariosoc.diacierre = @dayweek ) 
                       AND t365_horariosoc.id_cliente = @idcliente 
                ORDER  BY t365_horariosoc.horacierre ASC 

                IF @@ROWCOUNT > 0 
                  BEGIN 
                      IF @mincierre < CONVERT(TIME, @fechaevento) 
                         AND @maxcierre > CONVERT(TIME, @fechaevento)
            BEGIN
                        PRINT 'Cierre dentro de horario establecido' 
            END
                      ELSE 
                        BEGIN 
                            IF @mincierre > CONVERT(TIME, @fechaevento) 
                              BEGIN 
                                  PRINT 'Cierre Temprano' 

                                  EXEC Jssp_insertartramasistema 
                                    'Evento Horario', 
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

                                  EXEC Jssp_insertartramasistema 
                                    'Evento Horario', 
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
        SELECT @mincierre = Dateadd(mi, - 
                                    t365_horariosoc.toleranciacierre, 
                                           t365_horariosoc.horacierre), 
                       @maxcierre = Dateadd(mi, 
t365_horariosoc.toleranciacierre, 
                                    t365_horariosoc.horacierre), 
                       @idprotocolo = t365_clientes.id_protocolo 
                FROM   t365_horariosoc 
                       INNER JOIN t365_clientes 
                               ON t365_horariosoc.id_cliente = 
                                  t365_clientes.id_cliente 
                WHERE  
                       ( t365_horariosoc.diacierre = @dayweek ) 
                       AND t365_horariosoc.id_cliente = @idcliente 
                ORDER  BY t365_horariosoc.horacierre desc
          if @@ROWCOUNT > 0
          begin
               PRINT 'Cierre Tarde2' 

                                  EXEC Jssp_insertartramasistema 
                                    'Evento Horario', 
                                    @idcliente, 
                                    'E365_CIETARD', 
                                    '', 
                                    @idprotocolo, 
                                    @fechaevento, 
                                    ' ', 
                                    '1', 
                                    '100' 
          end
          else
                  BEGIN 
                      SELECT @idprotocolo = id_protocolo 
                      FROM   t365_clientes 
                      WHERE  id_cliente = @idcliente 

                      PRINT 'Cierre Fuera de Horario' 

                      EXEC Jssp_insertartramasistema 
                        'Evento Horario', 
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