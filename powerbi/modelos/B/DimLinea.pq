let
    Lineas = Table.Distinct(Table.SelectColumns(REGISTRO, {"LINEA DE NEGOCIO"})),
    Orden = Table.Sort(Lineas, {{"LINEA DE NEGOCIO", Order.Ascending}})
in
    Orden
