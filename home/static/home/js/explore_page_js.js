

$(document).ready(function () {
    handle_items_per_page_button();
 });


function handle_items_per_page_button()
{
    default_paginate_by=10
    if(window.location.href.indexOf("paginate_by=") == -1) //no option was selected - therefore default value is checked
    {
        document.getElementById("btnradio"+default_paginate_by).checked= true;
    }

    // find which value was selected before submitting and update the relevant radio button
    else
    {
        items_per_page_options=[5,10,15,20]
        for(i = 0; i < items_per_page_options.length; i++)
        {
            curr_option=items_per_page_options[i];
            if(window.location.href.indexOf("paginate_by="+curr_option) > -1)
            {
                document.getElementById("btnradio"+curr_option).checked= true;
            }
        }
    }
}

