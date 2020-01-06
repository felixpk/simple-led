$('document').ready(function () {
    let colorPicker = new iro.ColorPicker('#color-picker-container');
    colorPicker.on('input:end', onColorChange);

    function onColorChange() {
        $.post("/api/color", colorPicker.color.rgb)
    }

    $("#enable").click(function (e) {
        $.post("/api/color", colorPicker.color.rgb)
    });

    $("#disable").click(function (e) {
        $.get("/api/disable")
    });
});

$('#animationForm').submit(function (e) {
    e.preventDefault();
    let animation_selection = $("#animation").val();
    $.post("/api/animation/start", {"animation": animation_selection});
});

$('#animation').change(function (e) {
    $.get("/api/animation/options/" + $(this).val())
        .done(function (data) {
            console.log(data['options'][0])
        });
});