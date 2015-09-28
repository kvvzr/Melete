;(function(window, $) {
    'use strict';

    var moras = [8, 16, 32];
    var times = [1, 2];

    var mora = 8;
    var time = 1;

    var rhythms = [];

    $(document).ready(function() {
        initCreator(mora, time);
    });

    var initCreator = function(mora, time) {
        var $container = $('#rc-container');

        $container.empty();

        $container.append("<select id='mora-selector' class='selector'></select>");
        var $mora_selector = $('#mora-selector');
        for (var i = 0; i < moras.length; i++) {
            $mora_selector.append('<option data-content="<span data-mora=&quot;' + moras[i] + '&quot;>' + moras[i] + 'モーラ</span>">' + moras[i] + 'モーラ</option>');
        }
        $mora_selector.val(mora + 'モーラ');

        $container.append("<select id='time-selector' class='selector'></select>");
        var $time_selector = $('#time-selector');
        for (var i = 0; i < times.length; i++) {
            $time_selector.append('<option data-content="<span data-time=&quot;' + times[i] + '&quot;>' + times[i] + '小節</span>">' + times[i] + '小節</option>');
        }
        $time_selector.val(time + '小節');

        $('.selector').selectpicker({
            tickIcon: '',
        });

        $mora_selector.on('change', function(){
            mora = $('[data-id=mora-selector] > span > span').data('mora');
            initCreator(mora, time);
        });
        $time_selector.on('change', function(){
            time = $('[data-id=time-selector] > span > span').data('time');
            initCreator(mora, time);
        });

        $('#btn-create').off('click');
        $('#btn-create').on('click', function(event) {
            var pats = [[]];
            for (var j = 0; j < mora; j++) {
                var pat = [];
                for (var i = 0; i < mora * time; i++) {
                    if (rhythms[j][i]) {
                        pat.push(i * 48 * 4 / mora);
                    }
                }
                pats.push(pat);
            }
            var data = {
                division: 48,
                patterns: pats,
                nn: 4,
                dd: 2,
                time: time
            };
            $.post('/rhythm', {data: JSON.stringify(data)});
        });

        rhythms = new Array(mora);
        for (var i = 0; i < mora; i++) {
            $container.append('<p>' + (i + 1) + 'モーラ</p>');
            $container.append("<div class='rhythm-creator'></div>");
        }
        var $rhythm_creators = $('.rhythm-creator', $container);
        for (var j = 0; j < $rhythm_creators.length; j++) {
            var $node = $rhythm_creators.eq(j);
            new p5(function(p) {
                p.id = j;

                p.setup = function() {
                    p.createCanvas($node.width(), $node.height());
                    p.noStroke();
                    rhythms[p.id] = new Array(mora * time);
                    for (var i = 0; i < mora * time; i++) {
                        rhythms[p.id][i] = false;
                    }
                };

                p.draw = function() {
                    p.background(192);

                    p.rect(1, 1, p.height - 1, p.height - 2);
                    p.push();
                    p.fill(192);
                    p.translate(p.height / 2 - 2, p.height / 2);
                    p.rotate(p.radians(-30));
                    p.scale(p.height / 2);
                    p.triangle(0, -0.43, -0.5, 0.43, 0.5, 0.43);
                    p.pop();

                    for (var i = 0; i < mora * time; i++) {
                        if (rhythms[p.id][i]) {
                            p.fill(219, 228, 228);
                        } else {
                            p.fill(255);
                        }
                        p.rect(i * (p.width - p.height - 1) / (mora * time) + p.height + 1, 1, (p.width - p.height - 1) / (mora * time) - 1, p.height - 2);
                    }
                };

                p.mousePressed = function() {
                    for (var i = 0; i < mora * time; i++) {
                        if (i * (p.width - p.height) / (mora * time) + p.height < p.mouseX && p.mouseX < (i + 1) * (p.width - p.height) / (mora * time) + p.height && 1 < p.mouseY && p.mouseY < p.height) {
                            rhythms[p.id][i] = !rhythms[p.id][i];
                        }
                    }
                };

                p.windowResized = function() {
                    p.createCanvas($node.width(), $node.height());
                };
            }, $node.get(0));
        }
    };
})(this, jQuery);
