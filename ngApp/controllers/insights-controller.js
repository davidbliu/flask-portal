app.controller('InsightsController', function($scope, $http){
	$scope.getClicks = function(searchTerm){
		$http.get(ROOT_URL + '/api/golink_clicks?key='+encodeURIComponent(searchTerm)+'&token='+getToken()).
          success(function(data, status, headers, config){
          	$scope.clicks = data;
          	agData = aggregateClicks(data);
          	$scope.aggregatedClicks = agData['aggregates'];
          	$scope.clickHash = agData['clickHash'];
          }).
          error(function(data, status, headers, config){
            console.log('there was an error getting clicks');
          });
	}
	
});

function aggregateClicks(clicks){
	console.log('here');
	clickHash = {};
	keys = [];
	for(var i = 0; i < clicks.length; i++){
		email = clicks[i].email;
		if(keys.indexOf(email) == -1){
			clickHash[email] = [];
			keys.push(email);
		}
		clickHash[email].push(clicks[i])
	}
	aggregates = [];
	for(var i=0;i<keys.length;i++){
		aggregate = {'email': keys[i], 'num_clicks':clickHash[keys[i]].length}
		aggregates.push(aggregate);
	}
	console.log('here');
	return {'aggregates': aggregates, 'clickHash': clickHash};
}