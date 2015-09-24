ROOT_URL = 'http://testing.berkeley-pbl.com';
var token = '';
var app = angular.module('goApp', ['ngRoute']);
app.config(function($routeProvider) {
    $routeProvider
        .when('/', {
            templateUrl : 'views/home.html',
            controller  : 'GoController'
        })
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
app.controller("TokenController", function($scope){
  $scope.token = 'your token here';
  $scope.setToken=function(){
    token = $scope.token;
  } 
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
  function getUserClicks(email){
    $http.get(ROOT_URL + '/api/user_clicks?email='+email).
      success(function(data, status, headers, config){
        $scope.userClicks = data;
      }).
      error(function(data, status, headers, config){
        console.log('there was an error fetching user clicks');
      });
  }
  getUsers();
  $scope.title = 'Users Page'
  $scope.users = [];
  $scope.userClicks = [];
  $scope.pullUserClicks = function(email){
    console.log(email);
    console.log('pulling clicks');
    getUserClicks(encodeURIComponent(email));
  };
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
   	getGoLinks(1); // pull the first page of golinks when the page is first loaded
    $scope.firstName= "David";
    $scope.lastName= "Liu";
    $scope.filterName = 'filter pubs';
    $scope.permissionsOptions = ['Anyone', 'Only Me', 'Only PBL', 'Only Officers', 'Only Execs'];//[{'id': 'Only Me','label': 'Only Me'},{'id':' Only PBL', 'label':'Only PBL'}];//, 'Only Officers', 'Only Execs', 'Anyone'];
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
    $scope.saveGoLink = function(golink){
      id = golink.id;
      console.log('id was '+id);
      key = $('#'+id+'-key-input').val();
      description = $('#'+id+'-description-input').val();
      permissions = $("#" + id + "-permissions-input option:selected").text();
      url = $('#'+id+'-url-input').val();
      tags = $('#'+id+'-tags-input').val().split(',');
      golink.key = key;
      golink.url = url;
      golink.description = description;
      golink.permissions = permissions;
      golink.tags = tags;
      // save the link server side
      $.ajax({
        url: ROOT_URL+'/api/save_golink',
        type: 'POST',
        data: {'id': id, 'key':key, 
              'description': description, 
              'tags': tags.join(','), 
              'url': url,
              'permissions': permissions
        },
        success:function(data){
          console.log(data);
        },
        error:function (xhr, textStatus, thrownError){
          console.log('failed');
        }
      });
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