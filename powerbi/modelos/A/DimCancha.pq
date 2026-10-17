let
    Libro = Excel.Workbook(File.Contents(RutaExcel), null, true),
    Hoja = Libro{[Item="Canchas",Kind="Sheet"]}[Data],
    Cabeceras = Table.PromoteHeaders(Hoja, [PromoteAllScalars=true]),
    Tipos = Table.TransformColumnTypes(Table.SelectColumns(Cabeceras, {"Cancha", "Deporte"}, MissingField.Error), {{"Cancha", type text}, {"Deporte", type text}})
in
    Tipos
