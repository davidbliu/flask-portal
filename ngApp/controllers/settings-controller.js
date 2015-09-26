app.controller('SettingsController', function($scope, $http){
	$scope.registerPush = function(){
		console.log('registering push');
		console.log($scope.chromeID);
		$.ajax({
        url: ROOT_URL+'/api/register_push',
        type: 'POST',
        data: {'email': email, 'chrome_id':$scope.chromeID},
        success:function(data){
        	alert('successfully registered your chrome id');
          console.log(data);
        },
        error:function (xhr, textStatus, thrownError){
          console.log('failed to register push');
        }
      });
	}
});