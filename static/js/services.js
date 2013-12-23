var c3AppServices = angular.module('c3App.services', ['ngResource']);

c3AppServices.factory('JobRequest', ['$resource', function($resource) {
	return $resource( 'rest/v1/jobRequest/:jobId', 
		{ jobId: '@jobId' }, { 
			/*
			method1: { 
				method: 'PUT', 
				params: { bookId: '@bookId' }, 
				isArray: false 
			} */
			/* , method2: { ... } */
		} );
}]);