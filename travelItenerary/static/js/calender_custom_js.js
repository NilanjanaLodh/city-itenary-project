function getHour(time){
    return Math.trunc(time);
}

function getMinutes(time){
    return Math.round((time%1)*60);
}

function eventExists(POI_name, event_list){
    console.log(event_list);
    for(index in event_list){
        event = event_list[index];
        if(POI_name == event.title)
            return true;
    }
    return false;
}

function getEvent(event_title, event_list){
    for(index in event_list){
        if(event_list[index].title == event_title){
            // console.log(event_list[0].title);
            return index;
        }
    }
    return -1;
}

function createEventList(plan){
    let event_list = [];
    for(day=0; day<plan['tour'].length; day++){
            for(j=0; j<plan['tour'][day].length; j++){
            let event_object = {};
            let POI_start_date = new Date(plan['start_date']);
            POI_start_date.setDate(POI_start_date.getDate() + day);
            let POI_end_date = new Date(plan['start_date']);
            POI_end_date.setDate(POI_end_date.getDate() + day);

            let POI = plan['tour'][day][j];
            let visit_time = parseFloat(POI['time'])+9.0;
            let start_hour = getHour(visit_time);
            let start_min = getMinutes(visit_time);
            POI_start_date.setHours(start_hour);
            POI_start_date.setMinutes(start_min);
            // POI_start_date.setSeconds(0);
            POI_end_date.setHours(start_hour + Math.trunc(POI['time_spent']));
            POI_end_date.setMinutes(start_min + Math.round((POI['time_spent']%1)*60));
            // POI_end_date.setSeconds(0);

            event_object['title'] = POI['name'];
            event_object['start'] = POI_start_date;
            event_object['end'] = POI_end_date;
            // console.log(visit_time);
            event_object['editable'] = true;
            event_object['eventDurationEditable'] = true;
            event_object['eventStartEditable'] = true;
            event_object['overlap'] = false;
            event_list.push(event_object);
        }
    }
    return event_list;

}

function getEventObject(POI_name,start_date){
    let event_object = {};
    let POI_start_date = new Date(start_date);
    let POI_end_date = new Date(start_date);
    POI_end_date.setHours(POI_start_date.getHours() + 2);
    event_object.title = POI_name;
    event_object.start = moment(POI_start_date);
    event_object.end = moment(POI_end_date);
    event_object.editable = true;
    event_object.eventDurationEditable = true;
    event_object.eventStartEditable = true;
    event_object.overlap = false;
    return event_object;
}
    

function ajaxGetPOIall(plan){
    let city = plan['city'];
    let list_POI = [];
    $.ajax(
    {
        type: 'GET',
        url: '/iteneraryApplication/ajax/get_POI_all/',
        data: 
        {
            'city': city,
        },
        dataType: 'json',
                        
        success: function (data) {
            // console.log(data);
            list_POI = data;
        },
        async: false
    });

    return list_POI;
}

function remove_POI_from_plan(plan, event_title){
    let tour = plan['tour'];
    for(i in tour){
        let path = tour[i];
        for(j in path){
            let POI = path[j];
            if(POI['name'] == event_title)
                path.splice(j,1);
        }
    }
    return plan;
}

function get_POI_from_plan(plan,event_title){
    let tour = plan['tour'];
    for(i in tour){
        path = tour[i];
        for(j in path){
            let POI = path[j];
            if(POI['name'] == event_title)
                return POI;
        }
    }
    return -1;
}

$(document).ready(function() {
            let plan = JSON.parse(document.getElementById('plan').value);
            let event_list = createEventList(plan);
            let list_POI = ajaxGetPOIall(plan);
            var dataList = $("#results");
            dataList.empty();
            for(var name in list_POI){
                let opt = $("<option></option>").attr("value", list_POI[name]);
                dataList.append(opt);
            }

            $('#calendar').fullCalendar({
                schedulerLicenseKey: 'GPL-My-Project-Is-Open-Source',
                defaultView: 'agendaItenerary',
                defaultDate: plan['start_date'],
                events: event_list,
                eventResize: function(event, delta, revertFunc) {
                    
                    alert(event.title + " end is now " + event.end.format());
                    $.ajax({
                        type: 'POST',
                        url: '/iteneraryApplication/ajax/update_tour/',
                        data: {
                            'plan': JSON.stringify(plan),
                            'event_end': event.end.format(),
                            'event_start': event.start.format(),
                            'event_name' : event.title,
                            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                        },
                        dataType: 'json',
                        
                        success: function (data) {
                            // console.log(data);
                            plan = data;
                        },
                        error: function (data) {
                            alert("conflict found. reverting");
                            revertFunc();
                        }
                    });

                },
                eventDrop: function(event, delta, revertFunc) {
                    // console.log(event);

                    alert(event.title + " was dropped on " + event.start.format());
                    $.ajax({
                        type: 'POST',
                        url: '/iteneraryApplication/ajax/update_tour/',
                        data: {
                            'plan': JSON.stringify(plan),
                            'event_end': event.end.format(),
                            'event_start': event.start.format(),
                            'event_name' : event.title,
                            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                        },
                        dataType: 'json',
                        
                        success: function (data) {
                            // console.log(data);
                            plan = data;
                        },
                        error: function (data) {
                            alert("conflict found. reverting");
                            revertFunc();
                        }
                    });

                },
                eventAfterRender: function (event, element, view) {
                    let if_event_registered = false;
                    // console.log(event.title);
                    for(index in event_list){

                        if(event_list[index]['title']==event.title){
                            if_event_registered = true;
                            console.log(event_list[index]['title']);
                        }

                    }

                    if(!if_event_registered)
                    {
                        // console.log(event.title);
                        event_list.push(event);

                        $.ajax({
                            type: 'POST',
                            url: '/iteneraryApplication/ajax/update_tour/',
                            data: {
                                'plan': JSON.stringify(plan),
                                'event_end': event.end.format(),
                                'event_start': event.start.format(),
                                'event_name' : event.title,
                                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                            },
                            dataType: 'json',
                            
                            success: function (data) {
                                // console.log(data);
                                plan = data;
                            }
                        });
                    }
                },

                eventClick: function(calEvent, jsEvent, view) {
                    alert("model should show");
                    $('#infoModal').on('show.bs.modal', function (event) {
                       $(this).find('h4.modal-title').text(calEvent.title);
                    });
                    let POI = get_POI_from_plan(plan,calEvent.title);
                    console.log(POI);
                    // console.log(document.querySelector("#img_slide_0"));
                    document.querySelector("#img_slide_0").src = "/static/"+POI['images'][0];
                    document.querySelector("#img_slide_1").src = "/static/"+POI['images'][1];
                    document.querySelector("#img_slide_2").src = "/static/"+POI['images'][2];
                    $('#infoModal').find('.modal-document-body').text(POI['description']);
                    $('#infoModal').modal({show:true});

                },
                views: {
                    agendaItenerary: {
                        type: 'agenda',
                        duration: { days: plan['no_days'] },
                        buttonText: 'Itenerary'
                    }
                }
            });

            $('#add_button').click(function(e) {
                e.preventDefault();
                let POI_name = document.getElementById('addPOI').value;
                if(eventExists(POI_name,event_list))
                    alert("The place already exists in your itenerary");

                else{
                    let event_to_add = getEventObject(POI_name,plan['start_date']);
                    console.log()
                    $.ajax({
                        type: 'POST',
                        url: '/iteneraryApplication/ajax/update_tour/',
                        data: {
                            'plan': JSON.stringify(plan),
                            'event_end': event_to_add.end.format(),
                            'event_start': event_to_add.start.format(),
                            'event_name' : event_to_add.title,
                            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                        },
                        dataType: 'json',
                        
                        success: function (data) {
                            console.log(event_to_add['end'])
                            event_list.push(event_to_add);
                            $('#calendar').fullCalendar('renderEvent', event_to_add, stick=true);
                            console.log(event_list);
                            plan = data;
                        },
                        error: function (data) {
                            alert("conflict found. reverting");
                            // revertFunc();
                        }
                    });
                    
                }
            });

            $('#deleteEventButton').click(function(){
               let event_title = $('#infoModal').find('h4.modal-title').text();
               console.log(event_title);
               event_to_delete_index = getEvent(event_title,event_list);
               // console.log('123');
               event_list.splice(event_to_delete_index, 1);
               console.log(event_to_delete_index);
               $('#calendar').fullCalendar('removeEvents', function(eventObject) {
                    if(eventObject.title == event_title){
                        return true;
                    }
                    return false;
                });
               plan = remove_POI_from_plan(plan,event_title);
            });
        });