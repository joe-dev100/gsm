

function loadTables(columnIndex) {
    var oTable = $("#table").DataTable({
        "bFilter": true,
        "sDom": 'fBtlpi',
        "ordering": true,
        "aLengthMenu": [[10,20, 50, 100, 200, -1], [10,20, 50, 100, 200, "All"]],
        "iDisplayLength": 10,
        "bDestroy": true,
        "language": {
            search: ' ',
            sLengthMenu: '_MENU_',
            searchPlaceholder: "Search",
            sLengthMenu: 'Row Per Page _MENU_ Entries',
            info: "_START_ - _END_ of _TOTAL_ items",
            paginate: {
                next: ' <i class=" fa fa-angle-right"></i>',
                previous: '<i class="fa fa-angle-left"></i> '
            },
        },


        buttons: [
            {
                extend: "excel",
                class: "buttons-excel",
                init: function (api, node, config) {
                    $(node).hide();
                },
            },
            {
                extend: "pdf",
                class: "buttons-pdf",
                init: function (api, node, config) {
                    $(node).hide();
                },
            },
            {
                extend: "print",
                class: "buttons-print",
                init: function (api, node, config) {
                    $(node).hide();
                },
            },
        ],
        order: [],
        columnDefs: [
            {
                targets: "no-sort",
                orderable: false,
            },
        ],
        initComplete: (settings, json) => {
            $('.dataTables_filter').appendTo('#tableSearch');
            $('.dataTables_filter').appendTo('.search-input');
        },
    });

    // FILTRAGE PAR STATUT
    $(".filter-link").click(function () {
        var filter = $(this).data("filter");
        console.log(filter);
        if (filter == "All") {
            oTable.columns(columnIndex).search("").draw();
        } else {
            oTable.columns(columnIndex).search("^" + filter, true, false).draw();
        }
        
    });
    $("#btn_print").on("click", function () {
        oTable.button(".buttons-print").trigger();
    });
    $("#btn_pdf").on("click", function () {
        oTable.button(".buttons-pdf").trigger();
    });
    $("#btn_excel").on("click", function () {
        oTable.button(".buttons-excel").trigger();
    });

    var selectAllItems = "#select-all";
	var checkboxItem = ":checkbox";
	$(selectAllItems).on('click', function(){
		
		if (this.checked) {
		$(checkboxItem).each(function() {
			this.checked = true;
		});
		} else {
		$(checkboxItem).each(function() {
			this.checked = false;
		});
		}
		
	});
}

function selectStyle() {
    $('.select').select2({
        minimumResultsForSearch: -1,
        width: '100%'
      });
}

function setTitle(titleText) {
    
    document.title = titleText;
   
}

