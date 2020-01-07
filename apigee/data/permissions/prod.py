def resource_permissions(team_prefix):
    return {
      "resourcePermission" : [
      {
        "path" : "/",
        "permissions" : [ "get" ]
      },
      {
        "path" : "/apiproducts",
        "permissions" : [ "put", "get" ]
      },
      {
        "path" : "/apiproducts/*",
        "permissions" : [ ]
      },
      {
        "path" : "/apiproducts/" + team_prefix + "*/attributes",
        "permissions" : [ "put", "get" ]
      },
      {
        "path" : "/apiproducts/" + team_prefix + "*/attributes/*",
        "permissions" : [ "delete", "put", "get" ]
      },
      {
        "path" : "/apiproducts/" + team_prefix + "*",
        "permissions" : [ "delete", "put", "get" ]
      },
      {
        "path": "/environments/*/caches/" + team_prefix + "*",
        "permissions": [ "put", "get", "delete" ]
      },
      {
        "path": "/apiproxies/" + team_prefix + "*/maskconfigs",
        "permissions": [ "get", "put" ]
      },
      {
        "path" : "/environments/*/keyvaluemaps/" + team_prefix + "*",
        "permissions" : [ "put", "get" ]
      },
      {
        "path" : "/environments/*/keyvaluemaps/" + team_prefix + "*/entries",
        "permissions" : [ "put" ]
      },
      {
        "path" : "/developers/*/apps",
        "permissions" : [ "put", "get" ]
      },
      {
        "path" : "/developers/*/apps/" + team_prefix + "*",
        "permissions" : [ "delete", "put", "get" ]
      },
      {
        "path" : "/developers/*/apps/" + team_prefix + "*/attributes",
        "permissions" : [ "put", "get" ]
      },
      {
        "path" : "/developers/*/apps/" + team_prefix + "*/attributes/*",
        "permissions" : [ "delete", "put", "get" ]
      },
      {
        "path" : "/environments/*/caches",
        "permissions" : [ "put", "get" ]
      },
      {
        "path" : "/environments/*/caches/*",
        "permissions" : [ ]
      },
      {
        "path" : "/environments/*/caches/" + team_prefix + "*",
        "permissions" : [ "delete", "put", "get" ]
      },
      {
        "path" : "/environments/prod/applications/" + team_prefix + "*/revisions/*/debugsessions",
        "permissions" : [ "put", "get" ]
      },
      {
        "path" : "/environments/prod/applications/" + team_prefix + "*/revisions/*/debugsessions/*",
        "permissions" : [ "delete", "put", "get" ]
      },
      {
        "path" : "/environments/sandbox/applications/*/revisions/*/debugsessions",
        "permissions" : [ "put", "get" ]
      },
      {
        "path" : "/environments/sandbox/applications/*/revisions/*/debugsessions/*",
        "permissions" : [ "delete", "put", "get" ]
      }
     ]
    }
