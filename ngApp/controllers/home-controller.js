app.controller('HomeController', function($scope, $http) {
	function getRecentGolinks(){
		 $http.get(ROOT_URL + '/api/recent_golinks?&token='+getToken()).
    	success(function(data, status, headers, config){
    		$scope.golinks = data;
    	}).
    	error(function(data, status, headers, config){
    		console.log('there was an error');
    		console.log(data);
    	});
	}
  function searchGoPost(searchTerm){
    if(searchTerm.indexOf('#')!=-1){
      console.log('searching for the post');
        $http.get(ROOT_URL + '/api/get_link_post?search_term='+encodeURIComponent(searchTerm)+'&token='+getToken()).
          success(function(data, status, headers, config){
            if(data.content != null && data.content != ''){
              $('#search-post-div').html(data.content);
              $scope.searchPost = true;
            }
          }).
          error(function(data, status, headers, config){
            console.log('there was an error getting link post');
          });
    }
  }
	function searchGoLinks(searchTerm, page){
    $scope.searchPost = false;
    $('#search-post-div').html('');
		$http.get(ROOT_URL + '/api/search_golinks?search_term='+encodeURIComponent(searchTerm)+'&page=1&token='+getToken()).
    	success(function(data, status, headers, config){
    		$scope.golinks = data;
        $scope.searching = true;
        $scope.searchTerm = searchTerm;
    	}).
    	error(function(data, status, headers, config){
    		console.log('there was an error');
    		console.log(data);
    	});
    searchGoPost(searchTerm);
	}
    function getPopularLinks(){
      $http.get(ROOT_URL + '/api/popular_golinks?token='+getToken()).
      success(function(data, status, headers, config){
        $scope.popularLinks = data;
      }).
      error(function(data, status, headers, config){
        console.log('there was an error');
      });

    }
    function getTopRecent(){
      $http.get(ROOT_URL + '/api/top_recent?token='+getToken()).
      success(function(data, status, headers, config){
        $scope.topRecent = data;
      }).
      error(function(data, status, headers, config){
        console.log('top recent error');
      });
    };  
    getPopularLinks();
    // getGoLinks(1); // pull the first page of golinks when the page is first loaded
    getRecentGolinks();
    getTopRecent();

    $scope.tagCloud = getTagCloud();
    $scope.firstName= "David";
    $scope.lastName= "Liu";
    $scope.filterName = 'filter pubs';
    $scope.permissionsOptions = ['Anyone', 'Only Me', 'Only PBL', 'Only Officers', 'Only Execs'];//[{'id': 'Only Me','label': 'Only Me'},{'id':' Only PBL', 'label':'Only PBL'}];//, 'Only Officers', 'Only Execs', 'Anyone'];
    $scope.page = 1;

    searchGoPost("#pooble");
    $scope.searchGoLinks = function(){
    	console.log('this was called');
    	$scope.page == 1;
    	searchGoLinks($('#search-input').val(), 1);
    };
    $scope.getClicks = function(){
      $http.get(ROOT_URL + '/api/recent_clicks'). //?search_term='+searchTerm+'&page=1&token='+getToken()).
      success(function(data, status, headers, config){
        $scope.golinks = data;
      }).
      error(function(data, status, headers, config){
        console.log('there was an error');
        console.log(data);
      });
    }
    $scope.getPopular = function(){
      getPopularLink();
    };
    $scope.getImageSrc = function(type){
        return './images/box-icon.png';
    };
    $scope.image_hash = {}
      $scope.image_hash['document'] = 'docs-icon.png'
      $scope.image_hash['spreadsheets'] = 'sheets-icon.png'
      $scope.image_hash['facebook'] = 'facebook-icon.png'
      $scope.image_hash['trello'] = 'trello-logo.png'
      $scope.image_hash['youtube'] = 'youtube-icon.png'
      $scope.image_hash['box'] = 'box-icon.png'
      $scope.image_hash['piazza'] = 'piazza-icon.png'
      $scope.image_hash['flickr'] = 'flickr-logo.png'
      $scope.image_hash['git'] = 'git-icon.png'
      $scope.image_hash['other'] = 'pbl-logo.png'
      $scope.image_hash['drive'] = 'drive-icon.png'
      $scope.image_hash['instagram'] = 'instagram-logo.png'
      $scope.image_hash['presentation'] = 'sheets-icon.png'
      $scope.image_hash['form'] = 'forms-icon.png'
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
    $scope.deleteGoLink = function(golink){
      var r = confirm("Are you sure you want to delete: "+golink.key);
      if (r == true) {
        id = golink.id;
        $('#'+id+'-div').remove();
        $.ajax({
        url: ROOT_URL+'/api/delete_golink',
        type: 'POST',
        data: {'id': id},
        success:function(data){
          console.log(data);
        },
        error:function (xhr, textStatus, thrownError){
          console.log('failed');
        }
      });
      } else {
        console.log('aborted');
      }
      
    };
});