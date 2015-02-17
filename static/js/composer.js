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
            var chords_id = $('[data-id=chords-selector] > span > span').data('id');
            var rhythms_id = $('[data-id=rhythms-selector] > span > span').data('id');
            var nn = $('[data-id=time-selector] > span > span').data('nn');
            var dd = $('[data-id=time-selector] > span > span').data('dd');
            var range_high = $('[data-id=range-high-selector] > span > span').data('range-high');
            var range_low = $('[data-id=range-low-selector] > span > span').data('range-low');

            var data = [];
            $('.tune-detail').each(function(index, tune) {
                data.push({
                    lyric: $('.tune-lyric', tune).val(),
                    phoneme: $('.tune-phoneme', tune).val(),
                    chord_id: chords_id,
                    rhythm_id: rhythms_id,
                    nn: nn,
                    dd: dd,
                    skip_prob: 0.5,
                    bpm: $('.tune-bpm', tune).val(),
                    min_note: range_low,
                    max_note: range_high
                });
            });
            $.post('/compose', {title: $('#music-title').val(), data: JSON.stringify(data)}).done(function(data) {
                location.href = '/watch/' + data.music_id;
            });
        });
    });

    function loadPicker() {
        $('.selector').selectpicker({
            tickIcon: '',
        });
        $('#time-selector').selectpicker('val', '4 / 4');
    } 
})(this, jQuery);
