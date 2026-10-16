// Desarrollo posterior para datos sintéticos. Crear parámetro de texto RutaCSV.
let
    Origen = Csv.Document(File.Contents(RutaCSV), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Cabeceras = Table.PromoteHeaders(Origen, [PromoteAllScalars=true]),
    Tipos = Table.TransformColumnTypes(Cabeceras, {{"id", type text}, {"fecha", type date}, {"deporte", type text}, {"horas", type number}, {"monto_clp", Int64.Type}}, "en-US")
in
    Tipos
