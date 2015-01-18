;(function(window, $) {
    'use strict';

    $(document).ready(function() {
        loadPicker();

        $('#btn-analyze').on('click', function(event) {
            if (!$('#music-title').val() || !$('#music-lyrics').val()) {
                return;
            } 
            $('#tune-details').empty();
            $.post('/analyze_lyrics', {text: $('#music-lyrics').val()}).done(function(data) {
                $('#tune-details').append(tmpl($('#template-tunes').text(), data));
                loadPicker();
                $('#composer').carousel('next');
            });
        });

        $('#btn-compose').on('click', function(event) {
            var data = [];
            $('.tune-detail').each(function(index, tune) {
                data.push({
                    lyric: $('.tune-lyric', tune).val(),
                    phoneme: $('.tune-phoneme', tune).val(),
                    chord_id: 1,
                    rhythm_id: 1,
                    nn: 4,
                    dd: 2,
                    skip_prob: 0.5,
                    bpm: 120,
                    min_note: 72,
                    max_note: 93
                });
            });
            $.post('/compose', {title: $('#music-title').val(), data: JSON.stringify(data)}).done(function() {
            });
        });
    });

    function loadPicker() {
        $('.selectpicker').selectpicker();
    } 
})(this, jQuery);
