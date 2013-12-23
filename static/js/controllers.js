angular.module('c3App.controllers', ['c3App.services', 'ui.bootstrap'])

	.controller('c3PlotFormCtrl', ['$scope', '$http', 'JobRequest', function($scope, $http, JobRequest) {
		$scope.destination = undefined;
		$scope.departure = undefined;
		$scope.windowStart = undefined;
		$scope.windowStop = undefined;
		$scope.minTT = 120;
		$scope.maxTT = 240;

		$scope.objects = function(searchString) {
				return $http.get("rest/v1/objectSearch/"+searchString).then(function(response){
					return response.data;
			});
		}

		$scope.postJobRequest = function() {
			postData = {
				"fromId": 'myuserid',
				"departure": $scope.departure,
				"destination": $scope.destination,
				"windowStart": $scope.windowStart,
				"windowStop": $scope.windowStop,
				"minTT": $scope.minTT,
				"maxTT": $scope.maxTT
			}

			JobRequest.save({}, postData);
		}
	}])

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
	
