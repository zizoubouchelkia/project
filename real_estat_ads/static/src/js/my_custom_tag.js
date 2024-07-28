odoo.define('real_estat_ads.CustomAction', function(require) {
    "use strict";

    var AbstractAction = require('web.AbstractAction');
    var Core = require('web.core');

    var CustomAction = AbstractAction.extend({
        template: "CustomActions",
        start: function(){
            console.log("Action")
        }
    })

    Core.action_registry.add("custom_client_action",CustomAction)
})

