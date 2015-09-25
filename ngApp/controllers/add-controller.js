app.controller('AddController', function($scope){
  $scope.addGoLink = function(){
    key = $scope.goKey;
    url = $scope.goURL;
    //ajax request to save the golink
    $.ajax({
        url: ROOT_URL+'/api/add_golink',
        type: 'POST',
        data: {'key': key, 'url':url, 'email': email},
        success:function(data){
        	alert('successfully added ' + key);
        	$scope.key = '';
        	$scope.goURL = '';
        },
        error:function (xhr, textStatus, thrownError){
          console.log('failed');
        }
      });
  }
});