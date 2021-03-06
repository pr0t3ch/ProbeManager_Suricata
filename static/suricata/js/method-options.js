function fadeHttp() {
    django.jQuery(".field-uri").fadeIn("slow");
    django.jQuery(".field-scheduled_rules_deployment_enabled").fadeIn("slow");
    django.jQuery(".field-file").fadeOut("fast");
    django.jQuery(".field-data_type").fadeIn("slow");
}
function fade() {
    django.jQuery(".field-uri").fadeOut("fast");
    django.jQuery(".field-scheduled_rules_deployment_enabled").fadeOut("fast");
    django.jQuery(".field-scheduled_rules_deployment_crontab").fadeOut("fast");
    django.jQuery(".field-scheduled_deploy").fadeOut("fast");
    django.jQuery("#id_scheduled_deploy").prop("checked", false);
    django.jQuery("#id_scheduled_rules_deployment_enabled").prop("checked", false);
    django.jQuery(".field-data_type").fadeIn("slow");
}
function fadeFile() {
    django.jQuery(".field-file").fadeIn("slow");
    django.jQuery(".field-data_type").fadeIn("slow");
    fade();
}
function fadeMisp() {
     django.jQuery(".field-scheduled_rules_deployment_enabled").fadeIn("slow");
     django.jQuery(".field-file").fadeOut("fast");
     django.jQuery(".field-data_type").fadeOut("fast");
     django.jQuery(".field-data_type select").val("1");
}
function fadeElse() {
    django.jQuery(".field-file").fadeOut("fast");
    django.jQuery(".field-data_type").fadeIn("slow");
    fade();
}
function wraper() {
    if(django.jQuery( "#id_method option:selected" ).text() === "URL HTTP"){
        fadeHttp();
    }else if(django.jQuery( "#id_method option:selected" ).text() === "Upload file"){
        fadeFile();
    }else if(django.jQuery( "#id_method option:selected" ).text() === "MISP"){
        fadeMisp();
    }else{
        fadeElse();
    }
}
django.jQuery(document).ready(function(){
    django.jQuery("#id_scheduled_rules_deployment_enabled").change(function(){
        if(django.jQuery("#id_scheduled_rules_deployment_enabled").is(":checked")){
            django.jQuery(".field-scheduled_rules_deployment_crontab").fadeIn("slow");
            django.jQuery(".field-scheduled_deploy").fadeIn("slow");
        }else{
            django.jQuery(".field-scheduled_rules_deployment_crontab").fadeOut("fast");
            django.jQuery(".field-scheduled_deploy").fadeOut("fast");
            django.jQuery("#id_scheduled_deploy").prop("checked", false);
        }
    });
    wraper();
    django.jQuery("#id_method").change(function(){
        wraper();
    });
});
