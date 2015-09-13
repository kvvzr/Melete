;(function(window, $) {
    'use strict';

    $(document).ready(function() {
        initCreator($('.rc-container'), 8);
        $('.selector').selectpicker({
            tickIcon: '',
        });
    });

    var initCreator = function($container, count) {
        for (var i = 0; i < count - 1; i++) {
            $container.append('<p>' + (i + 1) + 'モーラ</p>');
            $container.append("<div class='rhythm-creator'></div>");
        }
        var $rhythm_creators = $('.rhythm-creator', $container);
        for (var j = 0; j < $rhythm_creators.length; j++) {
            var $node = $rhythm_creators.eq(j);
            new p5(function(p) {
                p.rhythms = [];

                p.setup = function() {
                    p.createCanvas($node.width(), $node.height());
                    p.noStroke();
                    for (var i = 0; i < count; i++) {
                        p.rhythms[i] = false;
                    }
                };

                p.draw = function() {
                    p.background(192);
                    for (var i = 0; i < count; i++) {
                        if (p.rhythms[i]) {
                            p.fill(219, 228, 228);
                        } else {
                            p.fill(255);
                        }
                        p.rect(i * (p.width - 1) / count + 1, 1, (p.width - 1) / count - 1, p.height - 2);
                    }
                };

                p.mousePressed = function() {
                    for (var i = 0; i < count; i++) {
                        if (i * p.width / count < p.mouseX && p.mouseX < (i + 1) * p.width / count && 1 < p.mouseY && p.mouseY < p.height) {
                            p.rhythms[i] = !p.rhythms[i];
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
