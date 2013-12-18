var c3App = angular.module('c3App', [
        'c3App.filters',
        'c3App.services',
        'c3App.directives',
        'c3App.controllers'
]);

c3App.config(function($routeProvider) {
        $routeProvider
	.when('', {
	        templateUrl: 'template/c3plot.html',
		controller: 'c3PlotCtrl'
	})
	.when('contact', {
	        templateUrl: 'template/c3contact.html',
		controller: 'c3ContactCtrl'
	})
	.when('about', {
	        templateUrl: 'template/c3about.html',
		controller: 'c3AboutCtrl'
	})
	.otherwise({
	        redirectTo: ''
	})
});
