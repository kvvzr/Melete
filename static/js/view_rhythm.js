;(function(window, $) {
    'use strict';

    $(document).ready(function() {
        var $button_fav = $('#btn-fav');
        $button_fav.on('click', function(event) {
            $.post('/star_rhythm', {rhythm_id: parseInt($button_fav.data('id'), 10)});
        });
    });
})(this, jQuery);
