app.controller('UsersController', function($scope, $http){
  function getMembers(){
     $http.get(ROOT_URL + '/api/current_members').
      success(function(data, status, headers, config){
        $scope.members = data;
      }).
      error(function(data, status, headers, config){
        console.log('there was an error');
      });
  }
  function getContributors(){
     $http.get(ROOT_URL + '/api/contributors').
      success(function(data, status, headers, config){
        $scope.contributors = data;
      }).
      error(function(data, status, headers, config){
        console.log('there was an error');
      });
  }
  function getContributions(email){
    $http.get(ROOT_URL + '/api/contributions?email='+encodeURIComponent(email)+'&token='+getToken()).
      success(function(data, status, headers, config){
        $scope.contributions = data;
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
  getContributors();
  $scope.title = 'Users Page'
  $scope.userClicks = [];
  getMembers();
  $scope.pullUserClicks = function(email){
    console.log(email);
    console.log('pulling clicks');
    getUserClicks(encodeURIComponent(email));
  };
  $scope.getContributions = function(email){
    $scope.contributor = email;
    $scope.showContributions=true;
    getContributions(email);
  };
});