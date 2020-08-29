window.onscroll = function(e) {
	var nav = document.getElementById('gnb');
	if (window.pageYOffset) {
		nav.classList.add('sticky');
	} else {
		nav.classList.remove('sticky');
	}
};

Number.prototype.pad = function(size) {
    var s = String(this);
    while (s.length < (size || 2)) {s = "0" + s;}
    return s;
};

function make_calendar(vars){
    var d = new Date();
    var month_name = ['January','February','March','April','May','June','July','August','September','October','November','December'];
    var month = d.getMonth();   //0-11
    var year = d.getFullYear(); //2014
    var first_date = month_name[month] + " " + 1 + " " + year;
    //September 1 2014
    var tmp = new Date(first_date).toDateString();
    //Mon Sep 01 2014 ...
    var first_day = tmp.substring(0, 3);    //Mon
    var day_name = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];
    var day_no = day_name.indexOf(first_day);   //1
    var days = new Date(year, month+1, 0).getDate();    //30
    //Tue Sep 30 2014 ...
    var calendar = get_calendar(day_no, days,vars);
    document.getElementById("calendar-month-year").innerHTML = month_name[month];
    document.getElementById("calendar-dates").appendChild(calendar);
		current_date();
}

function get_calendar(day_no, days, vars) {

	var day_name = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];

    if('31' in vars){ /** will return true if exist */
        console.log('Exist!');
       }

    var table = document.createElement('table');
    var tr = document.createElement('tr');

    //row for the day letters
    for(var c=0; c<=6; c++){
        var td = document.createElement('td');
				td.setAttribute("class", "days-of-week");
        td.innerHTML = day_name[c];
        tr.appendChild(td);
    }
    table.appendChild(tr);

    //create 2nd row
    tr = document.createElement('tr');
    var c;
    for(c=0; c<=6; c++){
        if(c == day_no){
            break;
        }
        var td = document.createElement('td');
        td.innerHTML = "";
        tr.appendChild(td);
    }

    var count = 1;

    for(; c<=6; c++){
        var td = document.createElement('td');
				td.setAttribute("class", "dates");
        if(count in vars){
        td.innerHTML = '<p>'+'0'+count+'</p><img src="'+vars[count]+'" data-toggle="modal" data-target="#myOutput'+count+'"/>';
        }
        else{
        td.innerHTML ='<a data-toggle="modal" data-target="#trial" class="open-AddBookDialog">'+'0'+count+'</a>';
        }
        count++;
        tr.appendChild(td);
    }
    table.appendChild(tr);

    //rest of the date rows
    for(var r=3; r<=7; r++){
        tr = document.createElement('tr');
        for(var c=0; c<=6; c++){
            if(count > days){
                table.appendChild(tr);
                return table;
            }
            var td = document.createElement('td');
						td.setAttribute("class", "dates");
						if(count in vars){
                td.innerHTML ='<p>'+(count).pad()+'</p><img src= "'+vars[count]+'" data-toggle="modal" data-target="#myOutput'+count+'"/>';
            } else {
                td.innerHTML ='<a data-toggle="modal" data-target="#trial" class="open-AddBookDialog">'+(count).pad()+'</a>';
            }
            count++;
            tr.appendChild(td);
        }
        table.appendChild(tr);
    }
    return table;
}

function current_date() {
	var days = new Date().getDate();
	var date_count = document.querySelectorAll('td.dates>a');
	var i = 0;
	for (var i=0; i<25;i++) {
		var day = date_count[i].innerHTML;
		if ((days).pad() === day) {
			date_count[i].classList.add("current_date");
		};
	};
}
//mark current dates
// const current_date = () => {
// 	var today = new Date();
// 	if () {
//
// 	}
// }
