


const full_name_field = $("#id_full_name")
const organisation_name = $("#id_organization_name")


if($("#id_is_organisation").is(":checked")) {
    full_name_field.addClass("d-none")
    organisation_name.removeClass("d-none")
}else{
    full_name_field.removeClass("d-none")
    organisation_name.addClass("d-none")
}

$("#id_is_organisation").on("change",function(target){
    if($(this).is(":checked")) {
        full_name_field.addClass("d-none")
        organisation_name.removeClass("d-none")
    }else{
        full_name_field.removeClass("d-none")
        organisation_name.addClass("d-none")
    }
})