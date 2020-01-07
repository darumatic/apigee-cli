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
        "path" : "/apiproducts/" + team_prefix + "*",
        "permissions" : [ "delete", "put", "get" ]
      },
      {
        "path" : "/applications",
        "permissions" : [ "put", "get" ]
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
        "path" : "/applications/*/revisions",
        "permissions" : [ "get" ]
      },
      {
        "path" : "/applications/" + team_prefix + "*/revisions/*",
        "permissions" : [ "put", "get", "delete" ]
      },
      {
        "path" : "/applications/" + team_prefix + "*",
        "permissions" : [ "put", "get", "delete" ]
      },
      {
        "path" : "/environments/*/caches/*",
        "permissions" : [ ]
      },
      {
        "path" : "/applications/*/deployments",
        "permissions" : [ "get" ]
      },
      {
        "path" : "/environments/*/deployments",
        "permissions" : [ "get" ]
      },
      {
        "path" : "/apiproducts/" + team_prefix + "*/attributes",
        "permissions" : [ "put", "get" ]
      },
      {
        "path" : "/apiproxies/" + team_prefix + "*/maskconfigs",
        "permissions" : [ "put", "get" ]
      },
      {
        "path" : "/environments/*/keyvaluemaps",
        "permissions" : [ "put", "get" ]
      },
      {
        "path" : "/environments/*/virtualhosts",
        "permissions" : [ "get" ]
      },
      {
        "path" : "/environments/*/caches/" + team_prefix + "*",
        "permissions" : [ "delete", "put", "get" ]
      },
      {
        "path" : "/environments/*/targetservers",
        "permissions" : [ "put", "get" ]
      },
      {
        "path" : "/apiproducts/" + team_prefix + "*/attributes/*",
        "permissions" : [ "delete", "put", "get" ]
      },
      {
        "path" : "/apiproxies/" + team_prefix + "*/maskconfigs/*",
        "permissions" : [ "delete", "put", "get" ]
      },
      {
        "path" : "/environments/*/virtualhosts/*",
        "permissions" : [ "get" ]
      },
      {
        "path" : "/environments/*/keyvaluemaps/" + team_prefix + "*",
        "permissions" : [ "delete", "put", "get" ]
      },
      {
        "path" : "/environments/*/keyvaluemaps/" + team_prefix + "*/entries",
        "permissions" : [ "put" ]
      },
      {
        "path" : "/environments/*/targetservers/" + team_prefix + "*",
        "permissions" : [ "delete", "put", "get" ]
      },
      {
        "organization": "snsw",
        "path": "/applications/*/revisions/*",
        "permissions": [ "put", "get", "delete" ]
      },
      {
        "path" : "/applications/*/revisions/*/deployments",
        "permissions" : [ "put", "get" ]
      },
      {
        "path" : "/environments/*/applications/*/deployments",
        "permissions" : [ "get" ]
      },
      {
        "path" : "/environments/*/keyvaluemaps/" + team_prefix + "*/entries/*",
        "permissions" : [ "delete", "put", "get" ]
      },
      {
        "path" : "/environments/*/applications/*/revisions/*/deployments",
        "permissions" : [ "get" ]
      },
      {
        "path" : "/environments/*/applications/" + team_prefix + "*/revisions/*/deployments",
        "permissions" : [ "delete", "put", "get" ]
      },
      {
        "path" : "/environments/dev/applications/*/revisions/*/deployments",
        "permissions" : [ "delete", "put", "get" ]
      },
      {
        "path" : "/environments/sit/applications/*/revisions/*/deployments",
        "permissions" : [ "delete", "put", "get" ]
      },
      {
        "path" : "/environments/prod/applications/" + team_prefix + "*/revisions/*/deployments",
        "permissions" : [ "delete", "put", "get" ]
      },
      {
        "path" : "/environments/dev/applications/*/revisions/*/debugsessions",
        "permissions" : [ "put", "get" ]
      },
      {
        "path" : "/environments/dev/applications/*/revisions/*/debugsessions/*",
        "permissions" : [ "delete", "put", "get" ]
      },
      {
        "path" : "/environments/sit/applications/*/revisions/*/debugsessions",
        "permissions" : [ "put", "get" ]
      },
      {
        "path" : "/environments/sit/applications/*/revisions/*/debugsessions/*",
        "permissions" : [ "delete", "put", "get" ]
      },
      {
        "path" : "/environments/test/applications/*/revisions/*/debugsessions",
        "permissions" : [ "put", "get" ]
      },
      {
        "path" : "/environments/test/applications/*/revisions/*/debugsessions/*",
        "permissions" : [ "delete", "put", "get" ]
      },
      {
        "path" : "/environments/sandbox/applications/*/revisions/*/debugsessions",
        "permissions" : [ "put", "get" ]
      },
      {
        "path" : "/environments/sandbox/applications/*/revisions/*/debugsessions/*",
        "permissions" : [ "delete", "put", "get" ]
      },
      {
        "path" : "/environments/sandbox/applications/*/revisions/*/deployments",
        "permissions" : [ "delete", "put", "get" ]
      },
      {
        "path" : "/environments/prod/applications/" + team_prefix + "*/revisions/*/debugsessions",
        "permissions" : [ "put", "get" ]
      },
      {
        "path" : "/environments/prod/applications/" + team_prefix + "*/revisions/*/debugsessions/*",
        "permissions" : [ "delete", "put", "get" ]
      }
     ]
    }
