angular.module('c3App.controllers', [])
        .controller('c3PlotCtrl', ['$scope', function($scope) {
	        $scope.model = {
		        message: 'Controller says Hi!'
		}
	}])
	.controller('c3MenuCtrl', ['$scope', '$location', function($scope, $location) {
	        $scope.isActive = function (viewLocation) {
		        return viewLocation === $location.path();
		};
	}])
	
