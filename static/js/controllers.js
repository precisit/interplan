angular.module('c3App.controllers', ['c3App.services', 'ui.bootstrap'])

	.controller('c3PlotFormCtrl', ['$scope', '$http', 'JobRequest', function($scope, $http, JobRequest) {
		$scope.destination = undefined;
		$scope.departure = undefined;
		$scope.windowStart = undefined;
		$scope.windowStop = undefined;
		$scope.minTT = 120;
		$scope.maxTT = 400;

		$scope.objects = function(searchString) {
				return $http.get("rest/v1/objectSearch/"+searchString).then(function(response){
					return response.data;
			});
		}

		$scope.postJobRequest = function() {
			//TODO: Generate RANDOM number / ID on this calculation
			postData = {
				"fromId": $("#c3Form input[name='myuserid']").val(),
				"departure": $scope.departure,
				"destination": $scope.destination,
				"windowStart": $("#c3Form input[name='start']").val(),
				"windowStop": $("#c3Form input[name='stop']").val(),
				"minTT": $scope.minTT,
				"maxTT": $scope.maxTT
			}

			console.log(postData);

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
	
