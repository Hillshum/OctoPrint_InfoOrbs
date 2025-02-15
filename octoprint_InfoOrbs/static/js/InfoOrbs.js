/*
 * View model for OctoPrint-InfoOrbs
 *
 * Author: Hilton Shumway
 * License: AGPLv3
 */
$(function() {
    function InfoorbsViewModel(parameters) {
        var self = this;

        self.settingsViewModel = parameters[0];

    }

    /* view model class, parameters for constructor, container to bind to
     * Please see http://docs.octoprint.org/en/master/plugins/viewmodels.html#registering-custom-viewmodels for more details
     * and a full list of the available options.
     */
    OCTOPRINT_VIEWMODELS.push({
        construct: InfoorbsViewModel,
        // ViewModels your plugin depends on, e.g. loginStateViewModel, settingsViewModel, ...
        dependencies: [ "settingsViewModel" ],
        // Elements to bind to, e.g. #settings_plugin_InfoOrbs, #tab_plugin_InfoOrbs, ...
        elements: [ /* ... */ ]
    });
});
