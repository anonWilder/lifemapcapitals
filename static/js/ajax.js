'use strict';
var empty = false;
var password = "",chk_password = "", value_empty = false;
var table = "";

var xhr = new XMLHttpRequest();

var form = new FormData();
var message = "";


$(".bts").click(function(e){
	$("#na").val('');
});

$(document).ready(function() {
	$('input[id="bts"]').attr('hidden', true);
	$('input[id="ac"]').on('keyup paste', function(){
		if ($(this).val ().length <= 6) {
			$('input[id="bts"]').attr('hidden', true);
			document.getElementById('bts').style.background="red"
			document.getElementById('bts').style.color="#fff"
			document.getElementById('bts').value="account not complete ..."
	  	}else{
	  		$('input[id="bts"]').attr('hidden', false);
	  		document.getElementById('bts').style.background="green"
	  		document.getElementById('bts').style.color="#fff"
	  		document.getElementById('bts').value="Click to autofill full name <<="
	  	}

	});

});

$('input[id="sd"]').attr('hidden', false);
$('input[id="bts"]').change(function(){
	if ($('input[id="bts"]').attr('hidden')=="hidden"){
		$('input[id="sd"]').attr('hidden', false);
	}else{
		$('input[id="sd"]').attr('hidden', true);
	}
		// $('').removeAttr('hidden');
});



$(document).ready(function(){

	var csrf = $("input[name=csrfmiddlewaretoken]").val();

	$(".bts").click(function(e){
		e.preventDefault();
		$.ajax({
			url:'/ajaxid/',
			async: false,
			cache:'false',
			type: 'get',
            dataType: "text",
			data: {
				ac_n: $(".io").val(),
	// 			'csrfmiddlewaretoken': csrf
			},
			success: function(data) {
				var mydata = JSON.parse(data);
				$('#na').val($('#na').val() + mydata[0].data);
			}
		})
	})
});

$(document).ready(function() {
	const name = document.getElementById('na')
  	$('form').on('submit', function(e){
  		if (name.value === '' || name.value == null || name.value == undefined) {
	  		e.preventDefault();
	    	swal('Name is required');
  	}
    if(!valid) {
      e.preventDefault();
    }
  });
});

$(document).ready(function() {
	const ac = document.getElementById('ac')
	const name = document.getElementById('na')
	const email = document.getElementById('em')
	const password = document.getElementById('pa')
	const form = document.getElementById('form')
	const errorElement = document.getElementById('error')
	form.addEventListener('submit', (e) => {
	  let messages = []
	  if (name.value === '' || name.value == null || name.value == undefined) {
	    messages.push('Full Name is required')
	  }

	  if (ac.value === '' || ac.value == null) {
	    messages.push('account is required')
	  }

	  // if (password.value.length <= 10) {
	  //   messages.push('Password must be longer than 6 characters')
	  // }

	  // if (password.value.length >= 10) {
	  //   messages.push('Password must be less than 20 characters')
	  // }

	  if (password.value === 'password') {
	    messages.push('Password cannot be password')
	  }

	  if (messages.length > 0) {
	    e.preventDefault()
	    errorElement.innerText = messages.join(', ')
	  }
	})

});


function _(id)
{	
	if(document.getElementById(id) == null)
		console(id);
	else
		return document.getElementById(id);
}
function hrm_alert(text,header="Good job!",type="success")
{	
	if(text != "VALUE INSERTED" || text != "UPDATE WAS SUCCESSFUL")
	{
		type = "warning"
		header="Error!"
	}
	
	if(text.includes('LOGIN WAS SUCCESSFUL'))
	{
		type = "success"
		header="SUCCESSFUL"
	}
	
	swal(header, text, type);
}

function alert(text,header="Error!",type="warning")
{
	if(text == "VALUE INSERTED" || text == "UPDATE WAS SUCCESSFUL")
	{
		type = "success"
		header="Good job!"
	}
	swal(header, text, type);
}

function hrm_prompt(text)
{

		let value = false
	swal({
                    title: "Are you sure?",
                    text: text,
                    icon: "warning",
                    buttons: true,
                    dangerMode: true,
                })
                .then((willDelete) => {
                    if (willDelete) {
                    	//// alert(willDelete)
                        this.value = willDelete
                    } else {
                        this.value = willDelete
                    }
                });
                return value
}
function select()
 {
   // alert("LOADED");
   // alert($(".title").val());
 }
// function// alert(text)
// {
// 		$("body").append("<div class=\"modal-backdrop fade in\"></div>");
// 			$("#myModal").addClass("in");
// 			$("#myModal").addClass("show");
// 			$("#myModal").css("display","block");
// 			$("#myModal").css("padding-right","14px");
// 			$(".modal-body").html(text);
			
// }

function getImageData(id,fid,oput)
{
//alert(document.getElementById(id).value);
		var reader = new XMLHttpRequest();
		var file = document.getElementById(fid);
$("body").append("<div id='loader'></div>");
var load = document.getElementById("loader");

var file = document.getElementById(fid);

var form = new FormData();
$("body").css("opacity","0.3");
form.append("file",file.files[0]);
console.log(file.files[0]);

reader.open("post","../classes/convert64.php",true);
reader.addEventListener("progress",function(e)
{	
	//###################################################
	load.style.display = "block";
load.style.position = "fixed";
load.style.backgroundColor = "#1ABC9C";
load.style.top = "0px";
load.style.left = "0px";
load.style.zIndex = "10000000";
load.style.transition = "0.3s";
load.style.height = "6px";

load.style.width = (e.loaded / e.total) * 100 + "%";
//################################################
console.log(e.loaded+"-"+e.total);
},false);

		reader.addEventListener("load",function(e)
		{
			$("body").css("opacity","1");
			load.style.width = (e.loaded / e.total) * 100 + "%";
			load.style.witdh = "100%";
			load.style.display = "none";

			var image = document.getElementById(oput);

			image.src = reader.responseText;


			image.setAttribute("alt","PLEASE SELECT AN IMAGE FILE");

			image.style.padding = "10%";
			image.style.fontWeight = "bold";
			image.style.color = "#00BCD4";

			image.addEventListener("click",function(e)
			{
				file.click();
			},false);

			console.log(reader.responseText);
			document.getElementById(id).value = reader.responseText;

			if((reader.responseText).substring(0,10) == "data:image" && !image.src == "")
				empty = false;
			else
				empty = true;

		});

		
		reader.send(form);


	}
	
function getMultiSelectVal()
{
            var obj = document.getElementsByClassName("multi_sel")[0];
            var sel = "";
            var count = 0;

            for(var i = 0; i < obj.options.length ; i++)
            {        
                    if(obj.options[i].selected == true)
                    {

                        ++count;
                    }        
            }

            for(var i = 0; i < obj.options.length ; i++)
            {        
                    if(obj.options[i].selected == true)
                    {
                    	if(count < 2)
                        sel += obj.options[i].innerHTML;
                    	else
                    		sel += obj.options[i].innerHTML + "$#";
                    }        
            }

            document.getElementById("multi").value = sel;
            console.log(sel);
}

function load()
{
	$.get("/active_customer",function(data){
		

		console.log(data)
// data = JSON.parse(data)
	$(".userdetails").each(function(e){
try{
	console.log(data[$(this).attr("data-name")])
	$(this).html(data[$(this).attr("data-name")])
}
catch(err)
{
	console.log(err)
}
		
	})
	

console.log(recieved)
})

	$(".load_options").each(function(e)
	{
		$(this).append("<i class=\"fa fa-spinner fa-spin loader\" style=\"font-size:24px\"></i>");
		alert("one Read");
	});

	  $(".table_search").on("keyup",function(e)
    {
        
      $(".tr_data").each(function(e)
      {
              
          $(this).show();


      });
      
      $(".tr_data").each(function(e)
      {
        var find = $(this).attr("name").toLowerCase();
          //alert()
        var mix = new RegExp($(".table_search").val().toLowerCase());
                
        if(!find.match(mix))
        {
          $(this).hide();
        }

        //console.log(find.match(mix));
        //console.log(mix);
      });
      //search = _("search_item").value;
      //Userfolder = _("User_folder").value;
      //Userfile = _("User_files").value;
      //$.post("upload_php_search.php", {"file": Userfile,"folder": Userfolder,"search": search} , Search_Result);
    });

	console.log("APP LOADED");
//NEW FUNCTIONS

$(".select-text").on("click",function(e)
{	
	$(this).select();
	console.log("WELCOME");
});


$(".feed").on('change',function(e){
	let rec = $($(this).attr("sub"))
	$.get($(this).attr('url')+"/"+$(this).val(),function(data){
		rec.html("")

		console.log(data.length)
// data = JSON.parse(data)
data.transformer.forEach(function(item)
{
	// console.log(rec)
	rec.append('<option value=' + item.id + '>' + item.name + '</option>');
})
	// for (var i = data.length - 1; i >= 0; i--) {
	// 	console.log(data[i])
		
	

	// }


	
})
})

$(".controller").on('change',function(e){
	let sel = $(this)
	console.log($(this).attr('value'));
	let values = JSON.parse($(this).attr('value'))
	values.forEach(function(item){
		try{
			console.log(item.option)
			console.log(sel.val())
			if (item.option == sel.val()){
				//classes to show
				for (var i = item.show.length - 1; i >= 0; i--) {
					$('.'+item.show[i]).show()
				}
				//classes to hide
				for (var i = item.hide.length - 1; i >= 0; i--) {
					$('.'+item.hide[i]).hide()
				}
			}
			else
			{
				for (var i = sel.attr('show').split(',').length - 1; i >= 0; i--) {
					console.log(sel.attr('show').split(',')[i])
				}
				//classes to hide
				for (var i = sel.attr('hide').split(',').length - 1; i >= 0; i--) {
					console.log(sel.attr('show').split(',')[i])
				}
			}
		}
		catch(err) {
			console.log(err.message)
		} 
	})

})

$(".reinvest").on("change", function(e)
{
	if($(this).is(":checked"))	
	{
		$(".reinvest_panel").append("<input type=\"hidden\" class=\"input reinvest_input\" value="+$(this).attr("amount")+"\" data-name=\"reinvest\">");
		$(".amount").removeAttr("required");
		$(".amount").removeAttr("type");
		$(".amount").css("border-color","#d2d6de");
	}
	else
	{
		$(".reinvest_input").remove();
		$(".amount").attr("required","required");
		$(".amount").attr("type","number");
	}
});

$(".multi_load").on("click",function(e){
	console.log("CAMED")
	let main = $($(this).attr("head"));
	console.log(main)
	let sub = $($(this).attr("subhead"));
	console.log(sub)
	main.append("<div class='multi_load multi_load"+$(".multi_load").length+"' ><hr/><a onclick=\"close_panel('.multi_load"+$(".multi_load").length+"')\" style='cursor:pointer;font-size:0.65em'>close</a>"+sub.html()+"</div>");
})

// $(".close_this").on
$(".upload").on("change", function(e)
{
	console.log("CAME HERE");
	$(this).append("<i class=\"fa fa-spinner fa-spin loader\" style=\"font-size:24px\"></i>");

					var reader = new FileReader();
var loaded = 0;
var load_class = $(this).attr("loader");
$(load_class).css("width",loaded+"%");
					$(load_class).html(loaded+"%");
					var output = document.getElementById($(this).attr("output"));
					var output_text = document.getElementById($(this).attr("output_text"));

					reader.addEventListener("load", function(){					
					output.src = reader.result;
					output_text.value = reader.result;
					$(load_class).css("width","100%");
					$(load_class).html(Math.round(100)+"%");
				});
					reader.addEventListener("progress", function(evt){					
					loaded = (evt.loaded / evt.total) * 100;
					console.log(loaded);
					$(load_class).css("width",loaded+"%");
					$(load_class).html(Math.round(loaded)+"%");
				});

				reader.readAsDataURL(e.target.files[0]);				
});
////////////////////////////////////
//#########################CREATE MODAL################################
/*$(".ph").attr("data-target","#myModal");
$(".ph").attr("data-toggle","modal");

$(".gh").attr("data-target","#myModal");
$(".gh").attr("data-toggle","modal");

$(".signup").attr("data-target","#myModal");
$(".signup").attr("data-toggle","modal");

$(".login").attr("data-target","#myModal");
$(".login").attr("data-toggle","modal");

$(".bonus").attr("data-target","#myModal");
$(".bonus").attr("data-toggle","modal");
*/

$(".ticket").on("click",function(e)
{
	//alert("WRKING");
	var id = $(this).attr("data-id");



//	_(id).style.display = 'block';	

//$(this).html("Loading...");
	$(this).addClass("warning");
	$(this).removeClass("ticket");

			//alert(data);
			//$(this).html("Loading...");
	$(this).removeClass("warning");
	$(this).addClass("ticket");

			location.replace("ticketdetails.php?edit="+id);		


});



// $("body").append("<div id=\"myModal\" style=\"z-index: 100000000;\" class=\"modal fade in\"  role=\"dialog\"><div class=\"modal-dialog\"><!--Modal content--><div class=\"modal-content\"><div class=\"modal-header\"><button type=\"button\" class=\"close\" data-dismiss=\"modal\" style=\"background-color: #000; \">close&times;</button><h4 class=\"modal-title\">Message Box</h4></div><div class=\"modal-body\"><p></p></div><div class=\"modal-footer\"></div></div></div></div>");
// $("body").append("<button id=\"click\" type=\"button\" style=\"display: none;\" data-target=\"myModal\" data-toggle=\"modal\"></button>");
// $("body").append("<div class=\"modal-backdrop fade in\"></div>");
$(".modal-backdrop").hide();
//Timer
count();

//############CREATE DATE VLUE FOR DATE DROP DOWN
	var date = new Date();


var year = date.getFullYear();

var year_up = year;
var year_down = year - 6;
//alert(year);

var year_val_up = "";
var year_val_down = "";


for(var i = 0; i < 5; ++i)
{
	var val = ++year_up;
	year_val_up += "<option value=" + val + ">" + val + "</option>";
}

for(var i = 0; i < 5; ++i)
{
	var val = ++year_down;
	year_val_down += "<option value=" + val + ">" + val + "</option>";
}
var year_sel = "<option selected value="+year+">"+year+"</option>"
$(".years").html(year_val_down+year_sel+year_val_up);

//###########################################################################
//GET TABLE 
$(".table > thead > th").each(function(e)
{

});
if(document.getElementById("table") != null)
{
	
	var counter = 0, datas = "id,", link= $(".table").attr("link"),table = $(".table").attr("data-name");	
	$("#table > thead th").each(function(e)
	{		
			if($(this).attr("data-name"))
			datas += $(this).attr("data-name")+",";	
	
	//
		++counter;
	});

	$.post("../classes/editform.php",{"readdata": datas, "table": table}, function(data)
	{
		var num = 0;	
		var number = 0;
		//
		//alert(data);
		var data_array = JSON.parse(data);		
		//
		//alert(typeof data_array);		
		//


		//alert(data_array[0].length);
		var tr = "";
		for(var i = 0; i < data_array.length; i++)
		{			 tr += "<tr class=\"table-row\">";
				
			var id = data_array[i][0];			
			for(var j = 1; j < data_array[i].length; j++)
			{	

				if(j == 1)
				tr += "<td>" + "<a href=\"" + link + "?edit=" + id + "\">" + data_array[i][j] + "</a></td>";
			else
				tr += "<td>" + data_array[i][j] + "</td>";
			}
			tr += "</tr>";

											
		}
		//alert(tr);
		document.getElementById("tbody").innerHTML = tr;		

			//if(number > 0)
			//{
			//	$(this).val(data_array[num]);
			//	++num;
			//}
			//++number;

		});
	}

//########################################

//#########################################################################
//Edit Form
if(document.getElementById("edit") != null)
{
	
	var counter = 0, datas = "", table = "", id = $("#edit").val();	

	$(".input").each(function(e)
	{
		$(this).addClass("fa");
		$(this).addClass("fa-spin");
		$(this).addClass("fa-spinner");
		if(counter > 0)
		{
			if($(this).attr("data-name"))
			datas += $(this).attr("data-name")+",";
		}
		else
		{			
			table += $(this).val();	
		}
	//
		++counter;		
	});

	let url = "../classes/editform.php";
	if($("#edit").attr("url") != undefined)
		url = $("#edit").attr("url");
	$.post(url,{"formdata": datas, "table": $('input[data-name="table"]').val(), "id": id,"csrfmiddlewaretoken":$('input[name="csrfmiddlewaretoken"]').val()}, function(data)
	{
		var num = 0;	
		var number = 0;
		//
		//alert(data);
		var data_array = data;		
		//
		//alert(typeof data_array);		
		//
		$(".input").each(function(e)
		{
			$(this).removeClass("fa");
		$(this).removeClass("fa-spin");
		$(this).removeClass("fa-spinner");
			if(number > 0)
			{
				if($(this).attr("type") == "password" || $(this).attr("data-name") == "table" || $(this).attr("noupdate") != undefined)
				{

				}												
				else
				{
					if($(this).attr("type") == "html")
				{
					$(this).html(data_array[$(this).attr("data-name")]);	
				}
				else
				{
					var is_element_sel = $(this).is("select");

					//// alert($(this).is("select"))
					if(is_element_sel)
					{
							//// alert(data_array[$(this).attr("data-name")]);
							$(this).parent().find(".select-dropdown").val(data_array[$(this).attr("data-name")])
					}
					let view = data_array[$(this).attr("data-name")];
					if (typeof view == 'boolean'){
						view = view.toString();
					}
					$(this).val(view);	
				}
							
			}
			++num;
			}
			++number;

		});
	});
}
//########################################
$("input").each(function(e)
{
	if($(this).attr("data-name") == "table")
		{
			table = $(this).val();
		}

	if($(this).attr("type") == "date")
	{
		$(this).attr("placeholder","mm/dd/yyyy");
	}

	if($(this).attr("type") == "number")
	{
		
	}
});

	$(".media-sel").on("change", function(e)
	{		
		switch(($(".media-sel").val()).toLowerCase())
		{
			case "announcement":
				$(".annouce").show();
				$(".media-file").hide();
			break;

			default:
			$(".annouce").hide();
			$(".media-file").show();
			break;
		}
	});
	$(".gh_ticket").on("keyup mousedown",function(e)
	{
		var str = 0;

		var g_help_per = parseInt($(this).attr("first-help"));
		var re_help_per = parseInt($(this).attr("recommit"));

		var recomit = 0;
		$(".gh_ticket").each(function(e)
		{

		if($(this).attr('gethelp') != undefined)
	{
		if($(this).val() == "")
		{
			str += 0;
		}			
		else
		{
			recomit += Math.round(parseInt($(this).val()) * (parseInt($(this).attr("recommit")) / 100));
	 		str += parseInt($(this).val());	 	
	 	}
	 //alert(str);

	}
});
		//alert(str);
		str += parseInt($(".gh_ticket").attr("left"));
		var left = (str % 1000);

		str = parseInt(str) - (str % 1000);	
		document.getElementById("left").innerHTML = left;
document.getElementById("total").innerHTML = str;
		document.getElementById("firsthelp").innerHTML =  Math.round(str * (parseInt($(this).attr("first-help")) / 100)) - (Math.round(str * (parseInt($(this).attr("first-help")) / 100)) % 500);
		console.log(str * (parseInt($(this).attr("first-help"))) / 100);
			if(recomit % 500 == 0)		
		document.getElementById("recommithelp").innerHTML = recomit;
	else
		document.getElementById("recommithelp").innerHTML = recomit + (500 - (recomit % 500));
		document.getElementById("secondhelp").innerHTML =str - parseInt(document.getElementById("firsthelp").innerHTML);

	});

$("input").on("keyup mousedown",function(e)
{
	//console.log($(this).val());
	/*if($(this).attr('gethelp') != undefined)
	{

		var str = parseInt($(this).val());
//		alert(str.length);
		var g_help_per = parseInt($(this).attr("first-help"));
		var re_help_per = parseInt($(this).attr("recommit"));

		document.getElementById("firsthelp").innerHTML = Math.round(str * (parseInt($(this).attr("first-help")) / 100));
		console.log(str * (parseInt($(this).attr("first-help"))) / 100);
		document.getElementById("recommithelp").innerHTML = Math.round(str * (parseInt($(this).attr("recommit")) / 100));
	}*/

	if($(this).attr('count') != undefined)
	{
		var str = $(this).val();
//		alert(str.length);
		document.getElementById($(this).attr('count')).innerHTML = str.length;
	}
	if($(this).attr("required") != undefined)
	{
		if($(this).val() == "")
		{
			$(this).css("border-bottom","1px solid red");
		}
		else
			$(this).css("border-bottom","1px solid #e0e0e0");
	}

	
		if($(this).attr("unique") != undefined)
{
	var field = $(this).attr("data-name");
	var data = $(this).val();
	var place = $(this);

	$.post("../classes/unique_field.php",{"field": field, "data": data, "table": table },function(data)
	{	
		//alert(data);
		if(parseInt(data) > 0)
		{
			place.attr("unique","Not Unique");
		//	console.log("Not In Unique");
		}
		else
		{	
		place.attr("unique","Unique");		
		}		
	},true);
	//console.log("Not Unique");
}		
});

$("textarea").on("keyup mousedown",function(e)
{
	//console.log($(this).val());
	if($(this).attr("required") != undefined)
	{
		if($(this).val() == "")
		{
			$(this).css("border","1px solid red");
		}
		else
			$(this).css("border","1px solid #e0e0e0");
	}
});

$(".gh").on("click",function(e)
{

	empty = false;
	validate();
	if(!empty)
	{	
		form.append("gh","gh");
		form.append("amount","0");
		var tickets = "";
		var ids = "";
		$(".gh_ticket").each(function(e)
		{
			if(parseInt($(this).val()) > 0 && $(this).val() != "")
			{	
				tickets += $(this).attr("data-id")+","+ $(this).val()+","+$(this).attr("real")+","+"#";				
			}
		});

		form.append("ph_id",tickets);
		//form.append("recomit",document.getElementById("recommithelp").value);
		//alert(tickets);
$(".gh").append("<div class=\"img-circle loader\" ><img src=\"../img/loader.gif\"/>");	

	xhr.addEventListener("load",function(e)
	{
	
	$(".loader").remove();
		document.getElementById("click").click();		
		$("body").append("<div class=\"modal-backdrop fade in\"></div>");
		$("#myModal").addClass("in");
		$("#myModal").css("display","block");
		$("#myModal").css("padding-right","14px");
			
		////hr.responseText);
		$(".modal-body").html(xhr.responseText);
		console.log(xhr.responseText);
	});
	
	xhr.open("post","../classes/dp_gh_class.php",true);
	xhr.send(form);		


	//if(true)
	//		//hr.responseText);
	//	else			
	////hr.status);
	}

if(value_empty)
$(".modal-body").html(message + "<br>Some Required Field's Are Empty");

});

$(".block").on("click",function(e)
{

	empty = false;
	validate();
	if(!empty)
	{	
		form.append("block","block");
		
$(this).append("<i class=\"fa fa-spinner fa-spin loader\" style=\"font-size:24px\"></i>");

	xhr.addEventListener("load",function(e)
	{
	
	$(".loader").remove();
		document.getElementById("click").click();		
		$("body").append("<div class=\"modal-backdrop fade in\"></div>");
		$("#myModal").addClass("in");
		$("#myModal").css("display","block");
		$("#myModal").css("padding-right","14px");
			
		////hr.responseText);
		$(".modal-body").html(xhr.responseText);
		console.log(xhr.responseText);
	});
	
	xhr.open("post","../classes/dp_gh_class.php",true);
	xhr.send(form);		


	//if(true)
	//		//hr.responseText);
	//	else			
	////hr.status);
	}

if(value_empty)
$(".modal-body").html(message + "<br>Some Required Field's Are Empty");

});

$(".memorandum").on("click",function(e)
{

	empty = false;
	validate();
	if(!empty)
	{	
		form.append("memorandum","block");
		
$(this).append("<div class=\"img-circle loader\" ><img src=\"../img/loader.gif\"/>");	

	xhr.addEventListener("load",function(e)
	{
	
	$(".loader").remove();
		document.getElementById("click").click();		
		$("body").append("<div class=\"modal-backdrop fade in\"></div>");
		$("#myModal").addClass("in");
		$("#myModal").css("display","block");
		$("#myModal").css("padding-right","14px");
			
		////hr.responseText);
		$(".modal-body").html(xhr.responseText);
		console.log(xhr.responseText);
	});
	
	xhr.open("post","../classes/dp_gh_class.php",true);
	xhr.send(form);		


	//if(true)
	//		//hr.responseText);
	//	else			
	////hr.status);
	}

if(value_empty)
$(".modal-body").html(message + "<br>Some Required Field's Are Empty");

});

$(".unmemorandum").on("click",function(e)
{

	empty = false;
	validate();
	if(!empty)
	{	
		form.append("unmemorandum","block");
		
$(this).append("<div class=\"img-circle loader\" ><img src=\"../img/loader.gif\"/>");	

	xhr.addEventListener("load",function(e)
	{
	
	$(".loader").remove();
		document.getElementById("click").click();		
		$("body").append("<div class=\"modal-backdrop fade in\"></div>");
		$("#myModal").addClass("in");
		$("#myModal").css("display","block");
		$("#myModal").css("padding-right","14px");
			
		////hr.responseText);
		$(".modal-body").html(xhr.responseText);
		console.log(xhr.responseText);
	});
	
	xhr.open("post","../classes/dp_gh_class.php",true);
	xhr.send(form);		


	//if(true)
	//		//hr.responseText);
	//	else			
	////hr.status);
	}

if(value_empty)
$(".modal-body").html(message + "<br>Some Required Field's Are Empty");

});



$(".unblock").on("click",function(e)
{

	empty = false;
	validate();
	if(!empty)
	{	
		form.append("unblock","unblock");
		
$(this).append("<i class=\"fa fa-spinner fa-spin loader\" style=\"font-size:24px\"></i>");

	xhr.addEventListener("load",function(e)
	{
	
	$(".loader").remove();
		document.getElementById("click").click();		
		$("body").append("<div class=\"modal-backdrop fade in\"></div>");
		$("#myModal").addClass("in");
		$("#myModal").css("display","block");
		$("#myModal").css("padding-right","14px");
			
		////hr.responseText);
		$(".modal-body").html(xhr.responseText);
		console.log(xhr.responseText);
	});
	
	xhr.open("post","../classes/dp_gh_class.php",true);
	xhr.send(form);		


	//if(true)
	//		//hr.responseText);
	//	else			
	////hr.status);
	}

if(value_empty)
$(".modal-body").html(message + "<br>Some Required Field's Are Empty");

});

$(".bonus").on("click",function(e)
{

	empty = false;
	validate();
	if(!empty)
	{	
		form.append("bonus","bonus");
		
	
$(this).append("<div class=\"img-circle loader\" ><img src=\"../img/loader.gif\"/>");
	xhr.addEventListener("load",function(e)
	{
		$(".loader").remove();
		document.getElementById("click").click();		
		$("body").append("<div class=\"modal-backdrop fade in\"></div>");
		$("#myModal").addClass("in");
		$("#myModal").css("display","block");
		$("#myModal").css("padding-right","14px");
		
		
		////hr.responseText);
		$(".modal-body").html(xhr.responseText);
		console.log(xhr.responseText);
	});
	
	xhr.open("post","../classes/dp_ph_class.php",true);
	xhr.send(form);		


	//if(true)
	//		//hr.responseText);
	//	else			
	////hr.status);
	}

if(value_empty)
alert(message + "<br>Some Required Field's Are Empty");

});

$(".signup").on("click",function(e)
{

	empty = false;
	validate();
	if(!empty)
	{					
	form.append("signup","bonus");

	$(".signup").val("Loading.....");
$(this).append("<i class=\"fa fa-spinner fa-spin loader\" style=\"font-size:24px\"></i>");

	xhr.addEventListener("load",function(e)
	{
	//	//hr.responseText);
		
		if(parseInt(xhr.responseText) == 1)
		{
			$(".loader").remove();
			document.getElementById("click").click();		
			$("body").append("<div class=\"modal-backdrop fade in\"></div>");
			$("#myModal").addClass("in");
			$("#myModal").css("display","block");
			$("#myModal").css("padding-right","14px");
			$(".modal-body").html("SIGN UP WAS SUCCESSFUL...<br/> <a href=\"crypto-dashboard\">click here</a> if page doesn't redirects");
			location.replace("../crypto-dashboard");
			console.log(xhr.responseText);
			$(".signup").val("Register");
		}
		else
		{
			$(".loader").remove();
			document.getElementById("click").click();		
			$("body").append("<div class=\"modal-backdrop fade in\"></div>");
			$("#myModal").addClass("in");
			$("#myModal").css("display","block");
			$("#myModal").css("padding-right","14px");
			$(".modal-body").html(xhr.responseText);
			//location.replace("../my_p_o/paymentoption.php");
			console.log(xhr.responseText);
			$(".si/gnup").val("Register");
		}
	
	});
	
	xhr.open("post","crypto-dashboard/classes/churchub_insert.php",true);
	xhr.send(form);		


	//if(true)
	//		//hr.responseText);
	//	else			
	////hr.status);
	}

if(value_empty)
alert(message + "<br>Some Required Field's Are Empty");

});


$(".verify").on("click",function(e)
{

	empty = false;
	validate();
	if(!empty)
	{					
	form.append("verify","bonus");

	$(".verify").val("Loading.....");
$(this).append("<i class=\"fa fa-spinner fa-spin loader\" style=\"font-size:24px\"></i>");

	xhr.addEventListener("load",function(e)
	{
	//	//hr.responseText);
		
		if(parseInt(xhr.responseText) == 1)
		{
			$(".loader").remove();
			document.getElementById("click").click();		
			$("body").append("<div class=\"modal-backdrop fade in\"></div>");
			$("#myModal").addClass("in");
			$("#myModal").css("display","block");
			$("#myModal").css("padding-right","14px");
			$(".modal-body").html("EMAIL WAS SUCCESSFULLY SENT...<br/>PLEASE KINDLY CHECK YOUR EMAIL OR RESEND.");
			//location.replace("../my_p_o/paymentoption.php");
			console.log(xhr.responseText);
			$(".verify").val("Verify Email");
		}
		else
		{
			$(".loader").remove();
			document.getElementById("click").click();		
			$("body").append("<div class=\"modal-backdrop fade in\"></div>");
			$("#myModal").addClass("in");
			$("#myModal").css("display","block");
			$("#myModal").css("padding-right","14px");
			$(".modal-body").html(xhr.responseText);
			//location.replace("../my_p_o/paymentoption.php");
			console.log(xhr.responseText);
			$(".verify").val("Verify Email");
		}
	
	});
	
	xhr.open("post",$(this).attr("data-ajax"),true);
	xhr.send(form);		


	//if(true)
	//		//hr.responseText);
	//	else			
	////hr.status);
	}

if(value_empty)
alert(message + "<br>Some Required Field's Are Empty");

});


$(".forgot").on("click",function(e)
{

	empty = false;
	validate();
	if(!empty)
	{					
	form.append("forgot","bonus");

	$(".forgot").val("Loading.....");
$(this).append("<i class=\"fa fa-spinner fa-spin loader\" style=\"font-size:24px\"></i>");

	xhr.addEventListener("load",function(e)
	{
	//	//hr.responseText);
		
		if(parseInt(xhr.responseText) == 1)
		{
			$(".loader").remove();
			document.getElementById("click").click();		
			$("body").append("<div class=\"modal-backdrop fade in\"></div>");
			$("#myModal").addClass("in");
			$("#myModal").css("display","block");
			$("#myModal").css("padding-right","14px");
			$(".modal-body").html("EMAIL WAS SUCCESSFULLY SENT...<br/>PLEASE KINDLY CHECK YOUR EMAIL OR RESEND.");
			//location.replace("../my_p_o/paymentoption.php");
			console.log(xhr.responseText);
			$(".verify").val("Verify Password");
		}
		else
		{
			$(".loader").remove();
			document.getElementById("click").click();		
			$("body").append("<div class=\"modal-backdrop fade in\"></div>");
			$("#myModal").addClass("in");
			$("#myModal").css("display","block");
			$("#myModal").css("padding-right","14px");
			$(".modal-body").html(xhr.responseText);
			//location.replace("../my_p_o/paymentoption.php");
			console.log(xhr.responseText);
			$(".verify").val("Verify Email");
		}
	
	});
	
	xhr.open("post",$(this).attr("data-ajax"),true);
	xhr.send(form);		


	//if(true)
	//		//hr.responseText);
	//	else			
	////hr.status);
	}

if(value_empty)
alert(message + "<br>Some Required Field's Are Empty");

});

$(".login").on("click",function(e)
{

	empty = false;
	validate();
	let login = $(this);
	if(!empty)
	{	
		form.append("login","bonus");
		
		$(".login").val("loading.......");
	$(this).append("<i class=\"fa fa-spinner fa-spin loader\" style=\"font-size:24px\"></i>");

	xhr.addEventListener("load",function(e)
	{
		$(".loader").remove();
		// document.getElementById("click").click();		
		// $("body").append("<div class=\"modal-backdrop fade in\"></div>");
		// $("#myModal").addClass("in");
		// $("#myModal").css("display","block");
		// $("#myModal").css("padding-right","14px");
		
		//hr.responseText);
		if(xhr.responseText == parseInt(1))
		{
			$(".login").val("login");
			xhr.responseText
		// $(".modal-body").html("LOGIN WAS SUCCESSFUL...<br/> <a href=\"crypto-dashboard/\">click here</a> if page doesn't redirects");
		hrm_alert("LOGIN WAS SUCCESSFUL...<br/> <a href=\"/account/\">click here</a> if page doesn't redirects");
		console.log(xhr.responseText);
		 location.replace("/account");
		}
		else
		{
			$(".login").val("login");
		//hr.responseText);
		// $(".modal-body").html(xhr.responseText);
		alert(xhr.responseText);
	}
	});
	if(login.attr("data-ajax") != undefined)
	{
		xhr.open("post",login.attr("data-ajax"),true);
	}
	else
	{
		xhr.open("post","crypto-dashboard/classes/dpclass.php",true);	
	}
	
	xhr.send(form);		


	//if(true)
	//		//hr.responseText);
	//	else			
	////hr.status);
	}

if(value_empty)
alert(message + "<br>Some Required Field's Are Empty");

});


$(".admin_login").on("click",function(e)
{

	empty = false;
	validate();
	if(!empty)
	{	
		form.append("admin_login","bonus");
		
		$(".admin_login").val("loading.......");
	$(this).append("<div class=\"img-circle loader\" ><img src=\"../img/loader.gif\"/>");

	xhr.addEventListener("load",function(e)
	{
		$(".loader").remove();
		document.getElementById("click").click();		
		$("body").append("<div class=\"modal-backdrop fade in\"></div>");
		$("#myModal").addClass("in");
		$("#myModal").css("display","block");
		$("#myModal").css("padding-right","14px");
		
		//hr.responseText);
		if(xhr.responseText == parseInt(1))
		{
			$(".admin_login").val("Login");
			xhr.responseText
		$(".modal-body").html("LOGIN WAS SUCCESSFUL...<br/> <a href=\"../dpadmin/\">click here</a> if page doesn't redirects");
		console.log(xhr.responseText);
		location.replace("../dpadmin");
		}
		else
		{
			$(".admin_login").val("login");
		//hr.responseText);
		$(".modal-body").html("Wrong username or password");
	}
	});
	
	xhr.open("post","../classes/dpclass.php",true);
	xhr.send(form);		


	//if(true)
	//		//hr.responseText);
	//	else			
	////hr.status);
	}

if(value_empty)
alert(message + "<br>Some Required Field's Are Empty");

});


$(".recomit").on("click",function(e)
{	
	empty = false;
	validate();
	if(!empty)
	{	
				$(this).append("<div class=\"img-circle loader\" ><img src=\"../img/loader.gif\"/>");
		form.append("recomit","recomit");

	xhr.addEventListener("load",function(e)
	{
	
		$(".loader").remove();
		document.getElementById("click").click();		
		$("body").append("<div class=\"modal-backdrop fade in\"></div>");
		$("#myModal").addClass("in");
		$("#myModal").css("display","block");
		$("#myModal").css("padding-right","14px");
	
		////hr.responseText);
		$(".modal-body").html(xhr.responseText);
		console.log(xhr.responseText);
	});
	
	xhr.open("post","../classes/dp_ph_class.php",true);
	xhr.send(form);		


	//if(true)
	//		//hr.responseText);
	//	else			
	////hr.status);
	}

if(value_empty)
alert(message + "<br>Some Required Field's Are Empty");

});

$(".ph").on("click",function(e)
{	
		empty = false;
	validate();
	if(!empty)
	{	
		form.append("ph","ph");
		
		$(".ph").append("<div class=\"img-circle loader\" ><img src=\"../img/loader.gif\"/>");

	xhr.addEventListener("load",function(e)
	{
		
		$(".loader").remove();
		document.getElementById("click").click();
		$("body").append("<div class=\"modal-backdrop fade in\"></div>");
		$("#myModal").addClass("in");
		$("#myModal").css("display","block");
		$("#myModal").css("padding-right","14px");


		////hr.responseText);
		$(".modal-body").html(xhr.responseText);
		if(xhr.responseText.trim() == "PH TICKET CREATED")
			location.replace(location.href);
		console.log(xhr.responseText);
	});
	
	xhr.open("post","../classes/dp_ph_class.php",true);
	xhr.send(form);		


	//if(true)
	//		//hr.responseText);
	//	else			
	////hr.status);
	}

if(value_empty)
alert(message + "<br>Some Required Field's Are Empty");

});

$(".match_user").on("click",function(e)
{	
		empty = false;
	validate();
	if(!empty)
	{	
		form.append("match_user","macth_user");
		
		$(".ph").append("<div class=\"img-circle loader\" ><img src=\"../img/loader.gif\"/>");

	xhr.addEventListener("load",function(e)
	{
		
		$(".loader").remove();
		document.getElementById("click").click();
		$("body").append("<div class=\"modal-backdrop fade in\"></div>");
		$("#myModal").addClass("in");
		$("#myModal").css("display","block");
		$("#myModal").css("padding-right","14px");


		////hr.responseText);
		$(".modal-body").html(xhr.responseText);
		if(xhr.responseText.trim() == "Matched")
			location.replace(location.href);
		console.log(xhr.responseText);
	});
	
	xhr.open("post","../classes/dp_ph_class.php",true);
	xhr.send(form);		


	//if(true)
	//		//hr.responseText);
	//	else			
	////hr.status);
	}

if(value_empty)
alert(message + "<br>Some Required Field's Are Empty");

});


$(".close").on("click",function(e)
{	
	$("#myModal").fadeOut(1000);
	$(".modal-backdrop").fadeOut(1000);
});

		$(".modal-backdrop").on("click",function(e)
{
$("#myModal").fadeOut(1000);
	$(".modal-backdrop").fadeOut(1000);

	alert("Clicked");
});


$(".submit").on("click",function(e)
{
	//alert(empty);


		
	empty = false;
	var confirm_submit = true;
if($(this).attr("prompt") != undefined)
{
	// if($(this).attr("sweetalert") != undefined)
	// {
	// 		confirm_submit = hrm_prompt($(this).attr("prompt"));
	// 		console.log("we"+confirm_submit);
	// }
	// else
	confirm_submit = confirm($(this).attr("prompt"));

}



	//Check For Unique Fields
	//alert(document.getElementsByClassName("input").length);

//alert(empty);
if(confirm_submit)
{

	if($(this).attr("special-form") != undefined)
{
	var s_class = $(this).attr("s_class");
	//alert("CAME");
	s_validate(s_class);
}
else
{
	validate()
}
if(!empty)
	{
			$(this).append("<i class=\"fa fa-spinner fa-spin loader\" style=\"font-size:24px\"></i>");

if($(this).attr("special-form") != undefined)
{
	
	var myform = special_form(s_class);

			//$(".submit")

			console.log(myform.pop);
	if($(this).attr("edit") != undefined)
	{
		myform.append("edit","true");
		myform.append("id",$(this).attr("edit"));
	}

	xhr.addEventListener("load",function(e)
	{
		console.log(xhr.responseText)
		
		////hr.responseText);
		$(".loader").remove();
		//document.getElementById("click").click();				

		$("#myModal").addClass("in");
		$("#myModal").addClass("show");
		$(".modal-backdrop").fadeIn(500);
	$("#myModal").fadeIn(500);	
		$("#myModal").css("padding-right","14px");


		if($(this).attr("new") == undefined)
		{
			console.log(xhr.responseText)

			//$(".modal-body").html(xhr.responseText);

			if(xhr.responseText.trim() =="VALUE INSERTED")
		{

hrm_alert(xhr.responseText)
			
			if($(this).attr("sweetalert") != undefined)
						{
							hrm_alert(xhr.responseText)
						}
			$(s_class).each(function(e)
				{
						if(!$(this).attr("type") == "hidden")
						{
								$(this).val("");
						}
				});							
			location.reload();

		}

		if(xhr.responseText.trim() =="UPDATE WAS SUCCESSFUL")
		{			
						hrm_alert(xhr.responseText)
			
			if($(this).attr("sweetalert") != undefined)
						{
							hrm_alert(xhr.responseText)
						}

				$(s_class).each(function(e)
				{
						if(!$(this).attr("type") == "hidden")
						{
								$(this).val("");
						}
				});							
			location.reload();
		}
		}
		else
		{
			var link = $(this).attr("new");			
		
			if(xhr.responseText.trim() =="VALUE INSERTED")
		{

hrm_alert(xhr.responseText)
			
			if($(this).attr("sweetalert") != undefined)
						{
							hrm_alert(xhr.responseText)
						}
			$(s_class).each(function(e)
				{
						if(!$(this).attr("type") == "hidden")
						{
								$(this).val("");
						}
				});							
			// location.reload();
					location.replace(link);
		}

		if(xhr.responseText.trim() =="UPDATE WAS SUCCESSFUL")
		{			
						hrm_alert(xhr.responseText)
			
			if($(this).attr("sweetalert") != undefined)
						{
							hrm_alert(xhr.responseText)
						}

				$(s_class).each(function(e)
				{
						if(!$(this).attr("type") == "hidden")
						{
								$(this).val("");
						}
				});							
			// location.reload();
			location.replace(link);
		}

			//alert("images/thumbs-up.png","Success",xhr.responseText + "<p><a class=\"success \" style=\"margin: 20px; font-size: 1.3em;\" href=\""+link+"> Next</a></p>");
			// $(".modal-body").html(xhr.responseText + "<p><a class=\"success \" style=\"margin: 20px; font-size: 1.3em;\" href=\""+link+"> Next</a></p>");
		}
		alert(xhr.responseText)
		console.log(xhr.responseText);
		
	});
	
	if($(this).attr("data-ajax") != undefined)
		xhr.open("post",$(this).attr("data-ajax"),true);
		else	
	xhr.open("post","../classes/churchub_insert.php",true);
	xhr.send(myform);		


	//if(true)
	//		//hr.responseText);
	//	else			
	////hr.status);
}
else
{
			//$(".submit")
	if(document.getElementById("edit") != null)
	{
		form.append("edit","true");
		form.append("id",$("#edit").val());
	}
	if($(this).attr('multi_app') != undefined)
	{

	let val = []
   $('.app').each(function(e){
      let appli =$(this).find('.appli').val()
      let number =$(this).find('.number').val()
      let watt =$(this).find('.watt').val()
      let inputs = {'table':'appliances_table','new_customer_ids':$("#edit").val(),'app_light_point':appli,'app_number':number,'app_watt':watt}
      val.push(inputs);


   })
   console.log(val)
	form.append($(this).attr('multi_app'),JSON.stringify(val));
	}
	xhr.addEventListener("load",function(e)
	{
		console.log(xhr.responseText)
		
		////hr.responseText);
		$(".loader").remove();
		// document.getElementById("click").click();				

		$("#myModal").addClass("in");
		$("#myModal").addClass("show");
		$(".modal-backdrop").fadeIn(500);
	$("#myModal").fadeIn(500);	
		$("#myModal").css("padding-right","14px");


		if(document.getElementById("new") == null)
		{
			console.log(xhr.responseText)
			// $(".modal-body").html(xhr.responseText);
			
			// if($(this).attr("sweetalert") != undefined)
			// 			{
			// 				hrm_alert(xhr.responseText)
			// 			}
				//	alert("images/thumbs-up.png","Success",xhr.responseText) 

			if(xhr.responseText.trim() =="VALUE INSERTED")
		{
			hrm_alert(xhr.responseText)
			$(".input").each(function(e)
				{
						if(!$(this).attr("type") == "hidden")
						{
								$(this).val("");
						}
				});							
			location.reload();

		}
		if(xhr.responseText.trim() =="UPDATE WAS SUCCESSFUL")
		{
			hrm_alert(xhr.responseText)
			$(".input").each(function(e)
				{
						if(!$(this).attr("type") == "hidden")
						{
								$(this).val("");
						}
				});							
			location.reload();
		}
		alert(xhr.responseText)
		}
		else
		{
			console.log(xhr.responseText)
						$(".modal-body").html(xhr.responseText);
						hrm_alert(xhr.responseText)

						if($(this).attr("sweetalert") != undefined)
						{
							hrm_alert(xhr.responseText)
						}
				//	alert("images/thumbs-up.png","Success",xhr.responseText) 

			if(xhr.responseText.trim() =="VALUE INSERTED")
		{
		
			if($(this).attr("success-text") != undefined)
			{
				hrm_alert($(this).attr("success-text"));
			}
			else
			{
				hrm_alert(xhr.responseText)
			}
			$(".input").each(function(e)
				{
						if(!$(this).attr("type") == "hidden")
						{
								$(this).val("");
						}
				});							
			var link = document.getElementById("new").value;			
			location.replace(link);			

		}
		if(xhr.responseText.trim() =="UPDATE WAS SUCCESSFUL")
		{
			if($(this).attr("success-text") != undefined)
			{
				hrm_alert($(this).attr("success-text"));
			}
			else{
				hrm_alert(xhr.responseText)
			}

			$(".input").each(function(e)
				{
						if(!$(this).attr("type") == "hidden")
						{
								$(this).val("");
						}
				});							
			var link = document.getElementById("new").value;			
			location.replace(link);			
		}

			alert(xhr.responseText)
			
					//alert("images/thumbs-up.png","Success",xhr.responseText + "<p><a class=\"success \" style=\"margin: 20px; font-size: 1.3em;\" href=\""+link+"> Next</a></p>");
			//$(".modal-body").html(xhr.responseText + "<p><a class=\"success \" style=\"margin: 20px; font-size: 1.3em;\" href=\""+link+"> Next</a></p>");
		}
		console.log(xhr.responseText);
		
	});
	if($(this).attr("data-ajax") != undefined)
		xhr.open("post",$(this).attr("data-ajax"),true);
		else	
	xhr.open("post","../classes/churchub_insert.php",true);
	xhr.send(form);		


	//if(true)
	//		//hr.responseText);
	//	else			
	////hr.status);
}
	}
}

if(value_empty)
{
	if($(this).attr("sweetalert") != undefined)
						{
							alert(message + "<br>Some Required Field's Are Empty","ERROR...","info")
						}
						empty = true;
// alert(message + "<br>Some Required Field's Are Empty");
alert(message + "<br>Some Required Field's Are Empty","ERROR...","info")
}


//alert(data.church_email);
/*$.post("churchub.php",data,function(dat)
{
	alert(dat);
});*/
		//alert(JSON.parse(data));	

});

$(".warning").on("click",function(e)
{
	//alert("images/warning.png","Warning","Currently Not Avialable");
});

$(".delete").on("click",function(e)
{
	//alert(empty);



	empty = false;
	//validate();

	//Check For Unique Fields
	//alert(document.getElementsByClassName("input").length);

//alert(empty);
if(!empty)
	{
		if($(this).attr("data-table") != undefined)
		{
		var run = confirm("ARE YOU SURE YOU WANT TO DELETE");
		if(run)
		{
			$(this).append("<i class=\"fa fa-spinner fa-spin loader\" style=\"font-size:24px\"></i>");
		
	
	form.append("delete","delete");
		form.append("table",$(this).attr("data-table"));
		form.append("id",$(this).attr("data-id"));
	

	xhr.addEventListener("load",function(e)
	{
		
		////hr.responseText);
		$(".loader").remove();
		document.getElementById("click").click();				
hrm_alert(xhr.responseText)
			if($(this).attr("sweetalert") != undefined)
						{
							hrm_alert(xhr.responseText)
						}

		$(".modal-body").html(xhr.responseText);
		$("#myModal").addClass("in");
		$(".modal-backdrop").fadeIn(500);
	$("#myModal").fadeIn(500);	
		$("#myModal").css("padding-right","14px");


			
		console.log(xhr.responseText);

		if(xhr.responseText.trim() == "DATA WAS SUCCESSFULLY DELETED")
		location.reload();
	});
	
	xhr.open("post","../classes/churchub_db_class.php",true);
	xhr.send(form);		


	//if(true)
	//		//hr.responseText);
	//	else			
	////hr.status);
}
	}

if(value_empty)
alert(message + "<br>Some Required Field's Are Empty");

//alert(data.church_email);
/*$.post("churchub.php",data,function(dat)
{
	alert(dat);
});*/
		//alert(JSON.parse(data));	
}
});

$(".claim").on("click",function(e)
{
	//alert(empty);



	empty = false;
	//validate();

	//Check For Unique Fields
	//alert(document.getElementsByClassName("input").length);

//alert(empty);
if(!empty)
	{
		if($(this).attr("data-amount") != undefined)
		{
		var run = confirm("ARE YOU SURE YOU WANT TO CLAIM YOUR SECOND GH");
		if(run)
		{
			$(this).append("<div class=\"img-circle loader\" ><img src=\"../img/loader.gif\"/>");
		
	
	form.append("claim","claim");
		form.append("amount",$(this).attr("data-amount"));
		form.append("id",$(this).attr("data-id"));
	

	xhr.addEventListener("load",function(e)
	{
		
		////hr.responseText);
		$(".loader").remove();
		document.getElementById("click").click();				

		$(".modal-body").html(xhr.responseText);
		$("#myModal").addClass("in");
		$(".modal-backdrop").fadeIn(500);
	$("#myModal").fadeIn(500);	
		$("#myModal").css("padding-right","14px");


			
		console.log(xhr.responseText);

		if(xhr.responseText.trim() == "UPDATE WAS SUCCESSFUL")
		location.reload();
	});
	
	xhr.open("post","../classes/churchub_db_class.php",true);
	xhr.send(form);		


	//if(true)
	//		//hr.responseText);
	//	else			
	////hr.status);
}
	}

if(value_empty)
alert(message + "<br>Some Required Field's Are Empty");

//alert(data.church_email);
/*$.post("churchub.php",data,function(dat)
{
	alert(dat);
});*/
		//alert(JSON.parse(data));	
}
});


$(".dissolve").on("click",function(e)
{
	
	empty = false;
	//validate();

if(!empty)
	{		
		if(true)
		{
		var run = confirm("ARE YOU SURE YOU WANT TO DIS-ENGAGE THIS TICKET");
		if(run)
		{
			$(this).append("<div class=\"img-circle loader\" ><img src=\"../img/loader.gif\"/>");
		
	
	form.append("dissolve","claim");		
		form.append("id",$(this).attr("data-id"));
	

	xhr.addEventListener("load",function(e)
	{
		
		////hr.responseText);
		$(".loader").remove();
		document.getElementById("click").click();				

		$(".modal-body").html(xhr.responseText);
		$("#myModal").addClass("in");
		$(".modal-backdrop").fadeIn(500);
	$("#myModal").fadeIn(500);	
		$("#myModal").css("padding-right","14px");


			
		console.log(xhr.responseText);

		if(xhr.responseText.trim() == "UPDATE WAS SUCCESSFUL")
		location.reload();
	});
	
	xhr.open("post","../classes/dp_gh_class.php",true);
	xhr.send(form);		


	//if(true)
	//		//hr.responseText);
	//	else			
	////hr.status);
}
	}

if(value_empty)
alert(message + "<br>Some Required Field's Are Empty");

//alert(data.church_email);
/*$.post("churchub.php",data,function(dat)
{
	alert(dat);
});*/
		//alert(JSON.parse(data));	
}
});



$(".reset").on("click",function(e)
{
	$(".input").val("");
});
$(".withdraw").on("click",function(e)
{
	//alert($(this).attr("data-id"));
$($(this).attr("data-id")).val($(this).attr("data-amount"));

var str = 0;

		var g_help_per = parseInt($(".gh_ticket").attr("first-help"));
		var re_help_per = parseInt($(".gh_ticket").attr("recommit"));
		var recomit = 0;
		$(".gh_ticket").each(function(e)
		{

		if($(this).attr('gethelp') != undefined)
	{
		if($(this).val() == "")
		{
			str += 0;
		}			
		else
		{
		 recomit += Math.round(parseInt($(this).val()) * (parseInt($(this).attr("recommit")) / 100));
		 //alert(recomit);
	 		str += parseInt($(this).val());	 	
		}
	 //alert(str);	 
	}
});
		str += parseInt($(".gh_ticket").attr("left"));
		var left = (str % 1000);
		str = parseInt(str) - (str % 1000);	
		document.getElementById("left").innerHTML = left;
document.getElementById("total").innerHTML = str;
				document.getElementById("firsthelp").innerHTML = Math.round(str * (parseInt($(".gh_ticket").attr("first-help")) / 100)) - (Math.round(str * (parseInt($(".gh_ticket").attr("first-help")) / 100)) % 500);
		console.log(str * (parseInt($(".gh_ticket").attr("first-help"))) / 100);
		if(recomit % 500 == 0)		
		document.getElementById("recommithelp").innerHTML = recomit;
	else
		document.getElementById("recommithelp").innerHTML = recomit + (500 - (recomit % 500));

		
		document.getElementById("secondhelp").innerHTML = str - parseInt(document.getElementById("firsthelp").innerHTML);
});
}

function validate()
{	
	message = "";
	value_empty = false;
var data = {
	table : "tbl_church",
	church: "SMHOS"
};
$(".input").each(function(e)
	{	
		if($(this).attr("unique") != undefined)
{
		if($(this).attr("unique") == "Not Unique")
		{
			value_empty = true;
			alert($(this).attr("label") + " already exist");
			message += $(this).attr("label") + " already exist" + "<br>";
		}
				
		}
	});

	$(".input").each(function()
	{
		if($(this).attr("data-name") == "table")
		{
			table = $(this).val();
		}
		//alert($(this).attr("required"));
if($(this).attr("required") != undefined)
{
	if($(this).val() == "")
	{
		empty = true;
		value_empty = true;
		$(this).css("border-bottom","1px solid red");
	}	
}

if($(this).attr("password") != undefined)
{
	password = $(this).val();	
}
//
if($(this).attr("chk_password") != undefined)
{
	chk_password = $(this).val();
}

//Validate For Numeric figures
if($(this).attr("type") == "number")
{
	var reg = /\d/;
	if(!reg.test($(this).val()))
	{
		var label = $(this).attr("label");
		alert(label +" is not a valid Number");
		message += label +" is not a valid Number" + "<br>";
		//console.log(label +" is not a valid Number");

	empty = true;		
	}
	else
	{
		if($(this).attr("min") != undefined)
		{
			if(parseInt($(this).attr("min")) > parseInt($(this).val()))
			{
				var label = $(this).attr("label");
		alert(label +" Must Not Be More Than "+ $(this).attr("min"));		
		message += label +" Must Not Be More Than "+ $(this).attr("min") + "<br>";
				

	empty = true
			}
		}
		if($(this).attr("max") != undefined)
		{
			if(parseInt($(this).attr("max")) < parseInt($(this).val()))
			{
				var label = $(this).attr("label");
		alert(label +" Must Not Be Lesser Than  "+ $(this).attr("max"));		
		message += label +" Must Not Be Lesser Than "+ $(this).attr("max") + "<br>";

	empty = true
			}
		}
	}

}

//Validate For Email figures
if($(this).attr("type") == "email")
{
	var reg = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;/^[a-zA-Z0-9]+$/
	if(!reg.test($(this).val()))
	{
		var label = $(this).attr("label");
		alert(label +" is not a valid email adddress");
		message += label +" is not a valid email adddress" + "<br>";
		console.log(label +" is not a valid email address");

	empty = true;		
	}
	else
	{
		if($(this).attr("min") != undefined)
		{
			if(parseInt($(this).attr("min")) > parseInt($(this).val()))
			{
				var label = $(this).attr("label");
		alert(label +" Must Not Be Lesser Than "+ $(this).attr("min"));		
		message += label +" Must Not Be Lesser Than "+ $(this).attr("min") + "<br>";

	empty = true
			}
		}
	}

}

//Validate For Email figures
if($(this).attr("type") == "username")
{
	var reg = /^[a-zA-Z0-9]+$/;
	if(!reg.test($(this).val()))
	{
		var label = $(this).attr("label");
		alert(label +" is not a valid username");
		message += label +" is not a valid username" + "<br>";
		console.log(label +" is not a valid username");

	empty = true;		
	}
	else
	{
		if($(this).attr("min") != undefined)
		{
			if(parseInt($(this).attr("min")) > parseInt($(this).val()))
			{
				var label = $(this).attr("label");
		alert(label +" Must Not Be Lesser Than "+ $(this).attr("min"));		
		message += label +" Must Not Be Lesser Than "+ $(this).attr("min") + "<br>";

	empty = true
			}
		}
	}

}

//Validate For Min Character
if($(this).attr("min-len") != undefined)
		{
			if(parseInt($(this).attr("min-len")) > $(this).val().length)
			{
				var label = $(this).attr("label");
		alert(label +" Must Not Be Lesser Than "+ $(this).attr("min-len") + " Character");		
		message += label +" Must Not Be Lesser Than "+ $(this).attr("min-len") + " Character" + "<br>";

	empty = true
			}
		}

//Validate For Current Password
if($(this).attr("match") != undefined)
{
	var label = $(this).attr("label");

	if($(this).attr("match") != $(this).val())
	{
		alert(label +" is An Incorrect Pin");
		hrm_alert(label +" is An Incorrect Pin","error","ERROR Message");
		console.log(label +" is An Incorrect Pin");
		message += label +" is An Incorrect Pin" + "<br>";
	empty = true;		
	}
}

//Validate For length Of password
if($(this).attr("length") != undefined)
{
	var label = $(this).attr("label");

	//alert($(this).val().length);
	if(parseInt($(this).attr("length")) != $(this).val().length)
	{
		alert(label +" is must not be less than " + parseInt($(this).attr("length")) + " Character");
		console.log(label +" is must not be less than " + parseInt($(this).attr("length")) + " Character");

		message += label +" is must not be less than " + parseInt($(this).attr("length")) + " Character" + "<br>";

	empty = true;		
	}
}
	//Validate For Dates
if($(this).attr("type") == "date")
{
	var label = $(this).attr("label");
	if(label == undefined)
		label = $(this).attr("placeholder");
	var reg = /\d{4}\/\d{2}\/\d{2}/;
	if(!reg.test($(this).val()))
	{
		
		// alert(label +" is not a valid Date " + $(this).val());
		console.log(label +" is not a valid Date");

		// message += label +" is not a valid Date" + "<br>";

	empty = false;		
	}
	else
	{
				var date = $(this).val().split("/");

//					alert(parseInt(date[0]));
				if(parseInt(date[0]) > 12)
				{
					alert("Month is not a valid ");
					message += "Month is not a valid " + "<br>";
					empty = true;
				}
				if(parseInt(date[1]) > 31)
				{
					alert("Day is not a valid");
					message += "Day is not a valid" + "<br>";
					empty = true;	
				}
				if(parseInt(parseInt(date[0])) == 2 && parseInt(date[1]) > 29)
				{					
					alert("Day is not a valid");
					message += "Day is not a valid" + "<br>";
					empty = true;		
				}				
	}
}

// if($(this).attr("type") == "checkbox")
// {}
	// console.log($(this).attr("data-name"));
if($(this).attr("data-name") != undefined && $(this).attr("type") != "checkbox")
{
	form.append($(this).attr("data-name"),$(this).val());


}

if($(this).attr("data-name") != undefined && $(this).attr("type") == "checkbox")
form.append($(this).attr("data-name"),$(this).is(":checked"));
	});

form.append('csrfmiddlewaretoken',$('input[name="csrfmiddlewaretoken"]').val());
console.log("Expected "+ $('input[name="csrfmiddlewaretoken"]').val())


	if(password != chk_password)
	{
		alert(password);
		alert(chk_password);
		alert("PASSWORD DOESN'T MATCH");
		message += "PASSWORD DOESN'T MATCH" + "<br>";
		empty = true;
		value_empty = true;
	}

}

function s_validate(s_class)
{			
	value_empty = false;
var data = {
	table : "tbl_church",
	church: "SMHOS"
};
$(s_class).each(function(e)
	{	
		if($(this).attr("unique") != undefined)
{
		if($(this).attr("unique") == "Not Unique")
		{
			empty = true;
			alert($(this).attr("label") + " already exist");
		}
				
		}
	});

	$(s_class).each(function()
	{
		if($(this).attr("data-name") == "table")
		{
			table = $(this).val();
		}
		//alert($(this).attr("required"));
if($(this).attr("required") != undefined)
{
	if($(this).val() == "")
	{
		empty = true;
		value_empty = true;
		$(this).css("border-bottom","1px solid red");
	}	
}

if($(this).attr("password") != undefined)
{
	password = $(this).val();	
}
//
if($(this).attr("chk_password") != undefined)
{
	chk_password = $(this).val();
}

//Validate For Numeric figures
if($(this).attr("type") == "number")
{
	var reg = /\d/;
	if(!reg.test($(this).val()))
	{
		var label = $(this).attr("label");
		alert(label +" is not a valid Number");
		console.log(label +" is not a valid Number");

	empty = true;		
	}
	else
	{
		if($(this).attr("min") != undefined)
		{
			if(parseInt($(this).attr("min")) > parseInt($(this).val()))
			{
				var label = $(this).attr("label");
		alert(label +" Must Not Be Lesser Than "+ $(this).attr("min"));		

	empty = true
			}
		}
	}

}

//Validate For Email figures
if($(this).attr("type") == "email")
{
	var reg = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;/^[a-zA-Z0-9]+$/
	if(!reg.test($(this).val()))
	{
		var label = $(this).attr("label");
		alert(label +" is not a valid email adddress");
		console.log(label +" is not a valid email address");

	empty = true;		
	}
	else
	{
		if($(this).attr("min") != undefined)
		{
			if(parseInt($(this).attr("min")) > parseInt($(this).val()))
			{
				var label = $(this).attr("label");
		alert(label +" Must Not Be Lesser Than "+ $(this).attr("min"));		

	empty = true
			}
		}
	}

}

//Validate For Email figures
if($(this).attr("type") == "username")
{
	var reg = /^[a-zA-Z0-9]+$/;
	if(!reg.test($(this).val()))
	{
		var label = $(this).attr("label");
		alert(label +" is not a valid username");
		console.log(label +" is not a valid username");

	empty = true;		
	}
	else
	{
		if($(this).attr("min") != undefined)
		{
			if(parseInt($(this).attr("min")) > parseInt($(this).val()))
			{
				var label = $(this).attr("label");
		alert(label +" Must Not Be Lesser Than "+ $(this).attr("min"));		

	empty = true
			}
		}
	}

}

//Validate For Current Password
if($(this).attr("match") != undefined)
{
	var label = $(this).attr("label");

	if($(this).attr("match") != $(this).val())
	{
		alert(label +" is An Incorrect Pin");
		console.log(label +" is An Incorrect Pin");

	empty = true;		
	}
}

//Validate For length Of password
if($(this).attr("length") != undefined)
{
	var label = $(this).attr("label");

	//alert($(this).val().length);
	if(parseInt($(this).attr("length")) != $(this).val().length)
	{
		alert(label +" is must not be less than " + parseInt($(this).attr("length")) + " Character");
		console.log(label +" is must not be less than " + parseInt($(this).attr("length")) + " Character");

	empty = true;		
	}
}
	//Validate For Dates
if($(this).attr("type") == "date")
{
	var label = $(this).attr("label");
	var reg = /\d{2}\/\d{2}\/\d{4}/;
	if(!reg.test($(this).val()))
	{
		
		alert(label +" is not a valid Date");
		console.log(label +" is not a valid Date");

	empty = true;		
	}
	else
	{
				var date = $(this).val().split("/");

//					alert(parseInt(date[0]));
				if(parseInt(date[0]) > 12)
				{
					alert("Month is not a valid ");
					empty = true;
				}
				if(parseInt(date[1]) > 31)
				{
					alert("Day is not a valid");
					empty = true;	
				}
				if(parseInt(parseInt(date[0])) == 2 && parseInt(date[1]) > 29)
				{
					alert("Day is not a valid");
					empty = true;		
				}				
	}

}
if($(this).attr("data-name") != undefined)
form.append($(this).attr("data-name"),$(this).val());
	});

	if(password != chk_password)
	{
		alert(password);
		alert(chk_password);
		alert("PASSWORD DOESN'T MATCH");
		empty = true;
		value_empty = true;
	}

}

function special_form(class_name)
{
	var s_form = new FormData();
	$(class_name).each(function()
	{
			if($(this).attr("data-name") != undefined)
s_form.append($(this).attr("data-name"),$(this).val());
	});

	return s_form;	
}
function _(id)
{
	if(document.getElementsByClassName(id) == null)
		console.log(id);
	else
		return document.getElementsByClassName(id);
}

function submited(id)
{
	_(id).onkeyup = function(e)
	{
		for(var i = 0; _(id).length < i; ++i)
		{
			if(_(id)[i].getAttribute("required") != undefined)
			{

				if(_(id)[i].value == "")
				{
					_(id)[i].style.border = "1px solid red";
				}
				else
					_(id)[i].style.border = "1px solid #e0e0e0";	
			}
		}


	};




var form = new FormData();

for(var i = 0; _(id).length > i; ++i)
	{
			if(_(id)[i].getAttribute("required") != undefined)
			{
				if(_(id)[i].value == "")
				{
					_(id)[i].style.border = "1px solid red";
				}
				else
					_(id)[i].style.border = "1px solid #e0e0e0";	
	}
}

for (var i = 0; _(id).length > i; ++i) {

	if(_(id)[i].getAttribute("required") != undefined)
			{
				if(_(id)[i].value == "")
				{
					_(id)[i].style.border = "1px solid red";
					empty = true;
				}				
}
form.append(_(id)[i].getAttribute("data-name"),_(id)[i].value);
}

if(!empty)
{
	xhr.open("post","../classes/churchub_insert.php",true);
	xhr.send(form);
				
}
else
alert(message + "<br>Some Required Field's Are Empty");

}

function reset(id)
{
	
	for (var i = 1; _(id).length > i; ++i) {
		//alert(_(id)[i].value);
		_(id)[i].value = "";
}
	
	

}

function updateId(e)
{
	if(document.getElementById("edit") != null)
{
	alert(e.value);
	var counter = 0, datas = "", table = "", id = e.value;	
	$(".input").each(function(e)
	{
		if(counter > 0)
		{
			if($(this).attr("data-name"))
			datas += $(this).attr("data-name")+",";
		}
		else
		{			
			table += $(this).val();	
		}
	//
		++counter;		
	});

	$.post("../classes/editform.php",{"formdata": datas, "table": table, "id": id}, function(data)
	{
		var num = 0;	
		var number = 0;
		//
		//alert(data);
		var data_array = JSON.parse(data);		
		//
		//alert(typeof data_array);		
		//
		$(".input").each(function(e)
		{
			if(number > 0)
			{
				if(data_array != null)
				$(this).val(data_array[num]);
				++num;
			}
			++number;

		});
	});
}
}

function count()
{

	setInterval(function()
	{
		$("h9").each(function()
		{

			var time = $(this).attr("data-count") - 1;

//			console.log(time);

var h = Math.floor(time / (60 * 60));


var min = Math.floor((time - (h * 60 * 60)) / 60);

var sec = Math.floor((time - (h * 60 * 60))) - (min * 60);

//console.log(Math.floor((time - (h * 60 * 60)) - 60));

//	console.log(min);
//	console.log(sec);

if(min < 0)
	min = 0;

if(sec < 0)
	sec = 0;

if(min < 10)
min = "0" + min;

if(h < 0)
	h = h;


if(h < 10 && h > -1)
h = "0" + h;


if(sec < 10)
sec = "0" + sec;

if(time > 0)
{
	//console.log(h);
	//console.log(min);
	//console.log(sec);
			
			
				$(this).html( h + "hr(s):" + min  + "min(s):" + sec + "sec");			
		}
		else
		$(this).html( "00" + "hr(s):" + "00"  + "min(s):" + "00" + "sec");				

			$(this).attr("data-count", time);
		});
	}, 1000);
}

function extend(id)
{
	var time = 0;
	$(".time").each(function(e)
	{
		if($(this).is(":checked"))
		{
			time = $(this).val();
		}
	});
var run = confirm("ARE YOU SURE WANT TO EXTEND TIME??");

if(run)
{
				$(this).append("<div class=\"img-circle loader\" ><img src=\"../img/loader.gif\"/>");
		var former = new FormData();

		former.append("transact_id",id);
			former.append("extendTime","true");		
			former.append("time",time);

	xhr.addEventListener("load",function(e)
	{
			$(".loader").remove();
		document.getElementById("click").click();		
		$("body").append("<div class=\"modal-backdrop fade in\"></div>");
		$("#myModal").addClass("in");
		$("#myModal").css("display","block");
		$("#myModal").css("padding-right","14px");
			

		
		$(".modal-body").html(xhr.responseText);
		location.reload();
		////hr.responseText);
		//console.log(xhr.responseText);
	});
	
	xhr.open("post","../classes/dpclass.php",true);
	xhr.send(former);		
}

}

function confirmPay(id)
{
	
var run = confirm("ARE YOU SURE WANT TO Confirm This Payment??\n Proccess Can't be Reversed!!!!");

if(run)
{
		var former = new FormData();

		former.append("transact_id",id);
			former.append("transaction","true");		

	xhr.addEventListener("load",function(e)
	{
		
		$(".modal-body").html(xhr.responseText);
		location.reload();
		////hr.responseText);
		//console.log(xhr.responseText);
	});
	
	xhr.open("post","../classes/dp_gh_class.php",true);
	xhr.send(former);		
}

}
function block(id)
{
	
var run = confirm("ARE YOU SURE WANT TO Disolve This Payment??\n Proccess Can't be Reversed!!!!");

if(run)
{
		var former = new FormData();

		former.append("transact_id",id);
			former.append("disolve","true");		

	xhr.addEventListener("load",function(e)
	{
		
		$(".modal-body").html(xhr.responseText);
		////hr.responseText);
		//console.log(xhr.responseText);

		location.reload();
	});
	
	xhr.open("post","../classes/dp_gh_class.php",true);
	xhr.send(former);		
}

}

function decline(id)
{
	
var run = confirm("ARE YOU SURE WANT TO Decline This Payment??\n Proccess Can't be Reversed!!!!");

if(run)
{
		var former = new FormData();

		former.append("transact_id",id);
			former.append("decline","true");		

	xhr.addEventListener("load",function(e)
	{
		
		$(".modal-body").html(xhr.responseText);
		////hr.responseText);
		//console.log(xhr.responseText);
	});
	
	xhr.open("post","../classes/dp_gh_class.php",true);
	xhr.send(former);		
}

}

function ph_detials(id)
{
		
	var former = new FormData();

		former.append("transact_id",id);
			former.append("ph_detials","true");		

	xhr.addEventListener("load",function(e)
	{


		////hr.responseText);
		$(".modal-body").html(xhr.responseText);

		$(".modal-body").html(xhr.responseText);
		////hr.responseText);
		//console.log(xhr.responseText);
	});
	
	xhr.open("post","../classes/dpclass.php",true);
	xhr.send(former);		

}

function gh_detials(id)
{
	
		
	var former = new FormData();

		former.append("transact_id",id);
			former.append("gh_detials","true");		

	xhr.addEventListener("load",function(e)
	{


		////hr.responseText);
		$(".modal-body").html(xhr.responseText);

		$(".modal-body").html(xhr.responseText);
		////hr.responseText);
		//console.log(xhr.responseText);
	});
	
	xhr.open("post","../classes/dpclass.php",true);
	xhr.send(former);		
}

function viewPop(id)
{
	

	var former = new FormData();

		former.append("transact_id",id);
			former.append("viewpop","true");		

	xhr.addEventListener("load",function(e)
	{
		
		$(".modal-body").html(xhr.responseText);
		////hr.responseText);
		//console.log(xhr.responseText);
	});
	
	xhr.open("post","../classes/dpclass.php",true);
	xhr.send(former);		

}

function viewAdminPop(id)
{
	

	var former = new FormData();

		former.append("transact_id",id);
			former.append("viewadminpop","true");		

	xhr.addEventListener("load",function(e)
	{
		
		$(".modal-body").html(xhr.responseText);
		////hr.responseText);
		//console.log(xhr.responseText);
	});
	
	xhr.open("post","../classes/dpclass.php",true);
	xhr.send(former);		

}


function upload()
{
	document.getElementById("file").click();

}


function deletePh(id)
{
	
var run = confirm("ARE YOU SURE YOU WANT TO CANCEL PH??");
if(run)
{
	var former = new FormData();

		former.append("ph_id",id);
			former.append("deletePh","true");		

	xhr.addEventListener("load",function(e)
	{
		
		$(".modal-body").html(xhr.responseText);
		////hr.responseText);
		//console.log(xhr.responseText);
		location.reload();
	});
	
	xhr.open("post","../classes/dp_ph_class.php",true);
	xhr.send(former);		
}
}

function updatePop(id)
{
	
	var former = new FormData();

		former.append("transact_id",id);
			former.append("pop","true");		
			former.append("img",document.getElementById('output').src);

	xhr.addEventListener("load",function(e)
	{
		
		$(".modal-body").html(xhr.responseText);
		////hr.responseText);
		//console.log(xhr.responseText);
	});
	
	xhr.open("post","../classes/dpclass.php",true);
	xhr.send(former);		

}

function updatePic()
{
	
	var former = new FormData();

		former.append("edit",$("#edit").val());
		former.append("id",$("#edit").val());
		former.append("table","tbl_user");
			
			former.append("picture",document.getElementById('output').src);

	xhr.addEventListener("load",function(e)
	{
		

		$(".modal-body").html(xhr.responseText);

			location.reload();
		////hr.responseText);
		//console.log(xhr.responseText);
	});
	
	xhr.open("post","../classes/churchub_insert.php",true);
	xhr.send(former);		

}

function readRecomit(user)
{
	
	$(".modal-body").html("<iframe style=\"border: none; width:100%; height: 450px;\" id=\"frame\" src=\"ghphchain.php?run=recomit&data-user="+user+"\"></iframe>");
$("body").css("opacity","0.4");
$("#frame").on("load",function(e)
{
	$("body").css("opacity","1");
		document.getElementById("click").click();		
		$("body").append("<div class=\"modal-backdrop fade in\"></div>");
		$("#myModal").addClass("in");
		$("#myModal").css("display","block");
		$("#myModal").css("padding-right","14px");
		

});

}

function readGh(user)
{
	
	$(".modal-body").html("<iframe style=\"border: none; width:100%; height: 450px;\" id=\"frame\" src=\"ghphchain.php?run=gh&data-user="+user+"\"></iframe>");
$("body").css("opacity","0.4");
$("#frame").on("load",function(e)
{
	$("body").css("opacity","1");
		document.getElementById("click").click();		
		$("body").append("<div class=\"modal-backdrop fade in\"></div>");
		$("#myModal").addClass("in");
		$("#myModal").css("display","block");
		$("#myModal").css("padding-right","14px");
		

});

}
function readPh(user)
{
	
	$(".modal-body").html("<iframe style=\"border: none; width:100%; height: 450px;\" id=\"frame\" src=\"ghphchain.php?run=ph&data-user="+user+"\"></iframe>");
$("body").css("opacity","0.4");
$("#frame").on("load",function(e)
{
	$("body").css("opacity","1");
		document.getElementById("click").click();		
		$("body").append("<div class=\"modal-backdrop fade in\"></div>");
		$("#myModal").addClass("in");
		$("#myModal").css("display","block");
		$("#myModal").css("padding-right","14px");
		

});

}
function extendView(id)
{
	
	var former = new FormData();

		former.append("transact_id",id);
			former.append("extend","true");					

	xhr.addEventListener("load",function(e)
	{
		
		$(".modal-body").html(xhr.responseText);
		////hr.responseText);
		//console.log(xhr.responseText);
	});
	
	xhr.open("post","../classes/dpclass.php",true);
	xhr.send(former);		


}
function paid()
{
		empty = false;
	validate();

	//Check For Unique Fields
	//alert(document.getElementsByClassName("input").length);

//alert(empty);
if(!empty)
	{
			$(".pay_btn").append("<div class=\"img-circle loader\" ><img src=\"../img/loader.gif\"/>");
	if(document.getElementById("edit") != null)
	{
		form.append("edit","true");
		form.append("id",$("#edit").val());
	}

	xhr.addEventListener("load",function(e)
	{
		
		////hr.responseText);
		$(".loader").remove();
		document.getElementById("click").click();				

		$("#myModal").addClass("in");
		$(".modal-backdrop").fadeIn(500);
	$("#myModal").fadeIn(500);	
		$("#myModal").css("padding-right","14px");


		if(document.getElementById("new") == null)
		$(".modal-body").html(xhr.responseText);
		else
		{
			var link = document.getElementById("new").value;			
			location.replace(link);
			alert("Cmae");
			$(".modal-body").html(xhr.responseText + "<p><a class=\"success \" style=\"margin: 20px; font-size: 1.3em;\" href=\""+link+"> Next</a></p>");
		}
		console.log(xhr.responseText);

		if(xhr.responseText.trim() =="VALUE INSERTED")
		{
			$(".input").val("");
			location.reload();

		}
		if(xhr.responseText.trim() =="UPDATE WAS SUCCESSFUL")
		{
			$(".input").val("");
			location.reload();
		}
	});
	
	xhr.open("post","../classes/churchub_insert.php",true);
	xhr.send(form);		


	//if(true)
	//		//hr.responseText);
	//	else			
	////hr.status);
	}

if(value_empty)
alert("Some Required Field's Are Empty");

//alert(data.church_email);
/*$.post("churchub.php",data,function(dat)
{
	alert(dat);
});*/
		//alert(JSON.parse(data));	


}

function upload(id)
{

            var file = document.getElementById('file').files[0];

            var form = new FormData();

            form.append("action","upload_pop");
            form.append("id",$("#file").attr("data-cir-id")); 

           // alert(id);           
            form.append("img",$(".fileinput-preview img").attr('src'));
            form.append("gh_to", $("#file").attr("data-gh-to"));

//e.target.innerHTML = "loading";

            _("loader_upload").style.display = 'block';
            

            
            form.append("file",file);


            var xml = new XMLHttpRequest();

                xml.addEventListener("progress",function(data)
            {
            	_("loader_upload").style.display = 'block';
             console.log(xml.responseText);
            },false);
            xml.addEventListener("load",function(data)
            {
                console.log(xml.responseText);
                _("loader_upload").style.display = 'none';                
               // alert(xml.responseText);
                close_alert();

            },false);

            xml.open("post","circleData.php",false);            
            xml.send(form);

}

function close_panel(class_var){
	$(class_var).remove();
}
function upload_pop(cir_id)
{
	//this.innerHTML = "loading";

	$(".alert-bar").fadeIn(1000);
	$(".alert-panel").fadeIn(1000);
            
            $(".upload-btn").attr("edit",cir_id);



}

function testify(text)
{

		$(".modal-body").html(text);
		$("#myModal").addClass("in");
		$(".modal-backdrop").fadeIn(500);
	$("#myModal").fadeIn(500);	
		$("#myModal").css("padding-right","14px");

}

function manageUserPop(doc)
{
	var username = doc.value;
	if(doc.value != "")
	location.replace("index.php?username="+username);
}

var churchub = {

	file : function(file){

	},
	
};

window.addEventListener('load',function(e)
{
	load();
	//// alert("WE ARE HERE");
});
