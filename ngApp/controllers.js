ROOT_URL = 'http://localhost:3001';

var app = angular.module('goApp', ['ngRoute']);
app.config(function($routeProvider) {
    $routeProvider
        // route for the home page
        .when('/', {
            templateUrl : 'views/home.html',
            controller  : 'GoController'
        })

        // route for the about page
        .when('/analytics', {
            templateUrl : 'views/analytics.html',
            controller  : 'AnalyticsController'
        })
        .when('/users', {
            templateUrl : 'views/users.html',
            controller  : 'UsersController'
        })
        .otherwise({
          'redirect_to': '/'
        });
});

app.controller('UsersController', function($scope, $http){
  function getUsers(){
     $http.get(ROOT_URL + '/api/main_users').
      success(function(data, status, headers, config){
        $scope.users = data;
      }).
      error(function(data, status, headers, config){
        console.log('there was an error');
      });
  }
  getUsers();
  $scope.title = 'Users Page'
  $scope.users = [];
});

app.controller('AnalyticsController', function($scope, $http){
  function getClicks(){
     $http.get(ROOT_URL + '/api/recent_clicks').
      success(function(data, status, headers, config){
        $scope.clicks = data;
      }).
      error(function(data, status, headers, config){
        console.log('there was an error');
      });
  }
  getClicks();
  $scope.title = 'Analytics Page'
  $scope.clicks = [];
});

app.controller('GoController', function($scope, $http) {
	function getGoLinks(page){
		 $http.get(ROOT_URL + '/api/all_golinks?page='+page.toString()+'&token='+getToken()).
    	success(function(data, status, headers, config){
    		$scope.golinks = data;
    		$scope.numLinks = data.length;
    	}).
    	error(function(data, status, headers, config){
    		console.log('there was an error');
    		console.log(data);
    	});
	}
	function searchGoLinks(searchTerm, page){
		$http.get(ROOT_URL + '/api/search_golinks?search_term='+searchTerm+'&page=1&token='+getToken()).
    	success(function(data, status, headers, config){
    		$scope.golinks = data;
    		$scope.numLinks = data.length;
    	}).
    	error(function(data, status, headers, config){
    		console.log('there was an error');
    		console.log(data);
    	});
	}
  function getDashboardLinks(){

  }
  function getPopularLinks(){

  }
   	getGoLinks(1); // pull the first page of golinks from the getgo
    $scope.firstName= "David";
    $scope.lastName= "Liu";
    $scope.filterName = 'filter pubs';
    $scope.page = 1;
    $scope.searchGoLinks = function(){
    	console.log('this was called');
    	$scope.page == 1;
    	searchGoLinks($('#search-input').val(), 1);
    };
    $scope.nextPage = function() {
    	$scope.page+=1
    	getGoLinks($scope.page);
    };
    $scope.getClicks = function(){
      $http.get(ROOT_URL + '/api/recent_clicks'). //?search_term='+searchTerm+'&page=1&token='+getToken()).
      success(function(data, status, headers, config){
        $scope.golinks = data;
        $scope.numLinks = data.length;
      }).
      error(function(data, status, headers, config){
        console.log('there was an error');
        console.log(data);
      });
    }
    $scope.getPopular = function(){
      getPopularLink();
    };
});



function toHex(str) {
    var result = '';
    for (var i=0; i<str.length; i++) {
      result += str.charCodeAt(i).toString(16);
    }
    return result;
  }
function getToken(){
  email = 'davidbliu@gmail.com';
  return toHex(email);
}