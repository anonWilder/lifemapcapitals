(function ($) {
    "use strict";
var editor;
 $('#example').DataTable({
    dom: 'Bfrtip',
                buttons: [
                    'copy', 'csv', 'excel', 'pdf', 'print'
                ],
     responsive: true
 });

//Consumption Ajax Table
 // $('#consumption').DataTable({
 //    dom: 'Bfrtip',
 //                buttons: [
 //                    'copy', 'csv', 'excel', 'pdf', 'print'
 //                ],
 //     responsive: true
 // });

$('#consumption').DataTable( {
	dom: 'Bfrtip',
                buttons: [
                    'copy', 'csv', 'excel', 'pdf', 'print'
                ],
     responsive: true,
        "ajax": "/get_table/"+$("#consumption").attr("query"),
        "columns": [
            { "data": "created_on" },
            { "data": "transformer_name" },
            { "data": "feeder_name" },
            { "data": "class" },
            { "data": "previous_read" },
            { "data": "current_read" },
            { "data": "consumed" },
            {"data": "amount"}            

        ]
    } );
 
 //Payment Ajax Table
// alert*("Camed")
$('#payments').DataTable( {
    dom: 'Bfrtip',
                buttons: [
                    'copy', 'csv', 'excel', 'pdf', 'print'
                ],
     responsive: true,
        "ajax": "/get_table/"+$("#payments").attr("query"),
        "columns": JSON.parse($("#payments").attr("datas"))
    } );
  

})(jQuery);
