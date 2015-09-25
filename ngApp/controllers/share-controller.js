app.controller('ShareController', function($scope, $http){
	function getMembers(){
		 $http.get(ROOT_URL + '/api/current_members').
		  success(function(data, status, headers, config){
		    $scope.members = data;
		  }).
		  error(function(data, status, headers, config){
		    console.log('there was an error');
		  });
	}
  	getMembers();
  	$scope.recipients = [];
  	$scope.hideMembers = false;
    $scope.addRecipient = function(member){
    	$scope.recipients.push(member);
    	index = $scope.members.indexOf(member);
    	if (index > -1) {
		    $scope.members.splice(index, 1);
		}
    }
    $scope.removeRecipient = function(member){
    	$scope.members.push(member);
    	index = $scope.recipients.indexOf(member);
    	if (index > -1) {
		    $scope.recipients.splice(index, 1);
		}
    }
    $scope.sendPush = function(){
    	recipientEmails = $scope.recipients.map(function(x){
    		return x.email;
    	});
    	message = $scope.message;
    	links = $scope.links;
    	$scope.pushMessage = 'pushing out notification...';
    	$.ajax({
        url: ROOT_URL+'/api/send_push',
        type: 'POST',
        data: {'recipients': recipientEmails, 'message':message, 
              'links': links, 
              'email': email
        },
        success:function(data){
        	$('#pushMessage').text(data.body);
          console.log('successfully send push');
          console.log(data);
        },
        error:function (xhr, textStatus, thrownError){
          console.log('failed');
        }
      });
    }
});