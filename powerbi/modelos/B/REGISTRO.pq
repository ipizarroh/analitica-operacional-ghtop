let
    Libro = Excel.Workbook(File.Contents(RutaExcel), null, true),
    Hoja = Libro{[Item="REGISTRO",Kind="Sheet"]}[Data],
    Cabeceras = Table.PromoteHeaders(Table.Skip(Hoja,1), [PromoteAllScalars=true]),
    Contrato = Table.SelectColumns(Cabeceras, {"FECHA", "MES", "DIA", "EMPRESA", "HORA INICIO", "HORA FIN", "LINEA DE NEGOCIO", "SUBLINEA DE NEGOCIO", "DETALLE", "CANCHA", "CLIENTE", "MONTO COBRADO", "EFECTIVO RECIBIDO", "MONTO RECIBIDO MP", "IVA", "NETO SIN IVA", "Participación administración (demo)", "ID movimiento (demo)"}, MissingField.Error),
    Tipos = Table.TransformColumnTypes(Contrato, {{"FECHA", type date}, {"MES", type text}, {"DIA", type text}, {"EMPRESA", type text}, {"HORA INICIO", type time}, {"HORA FIN", type time}, {"LINEA DE NEGOCIO", type text}, {"SUBLINEA DE NEGOCIO", type text}, {"DETALLE", type text}, {"CANCHA", type text}, {"CLIENTE", type text}, {"MONTO COBRADO", Currency.Type}, {"EFECTIVO RECIBIDO", Currency.Type}, {"MONTO RECIBIDO MP", Currency.Type}, {"IVA", Currency.Type}, {"NETO SIN IVA", Currency.Type}, {"Participación administración (demo)", Currency.Type}, {"ID movimiento (demo)", type text}}, "es-CL"),
    Fechas = Table.SelectRows(Tipos, each [FECHA] <> null),
    Universo = Table.SelectRows(Fechas, each [LINEA DE NEGOCIO] <> "TIENDA" and not List.Contains({"PAGO G3", "COPA LITORAL"}, [SUBLINEA DE NEGOCIO])),
    Normalizado = Table.ReplaceValue(Universo, "ESCALERILLA", "ESCALERILLA TENIS", Replacer.ReplaceText, {"LINEA DE NEGOCIO"})
in
    Normalizado
