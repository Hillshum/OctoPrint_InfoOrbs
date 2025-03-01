/*
 * View model for OctoPrint-InfoOrbs
 *
 * Author: Hilton Shumway
 * License: AGPLv3
 */
$(function() {

    CORNERS_KEYS = ['top_left_x', 'top_left_y', 'bottom_right_x', 'bottom_right_y'];
    function InfoorbsViewModel(parameters) {
        var self = this;

        self.settingsViewModel = parameters[0];

        self.onBeforeBinding = () => {
            self.settings = self.settingsViewModel.settings.plugins.InfoOrbs;
        }

        self.reloadImage = async () => {
            let url = '/plugin/InfoOrbs/snapshot';
            let response = await fetch(url);
            let blob = await response.blob();
            console.log('reloding image');
        }

        self.previewUrl = ko.pureComputed(function() {
            const params = new URLSearchParams();

            CORNERS_KEYS.forEach((key) => {
                params.append(key, self.settings[key]());
            });

            return `/plugin/InfoOrbs/snapshot?${params.toString()}`;
        });

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
        elements: ['#settings_plugin_InfoOrbs']
    });
});
