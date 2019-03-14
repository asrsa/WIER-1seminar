# TODO crawler implementation
#   get frontier, set:
#                 HTML  če je htmlContetn not null -> init frontier
#                 BINARY ce je null -> download binary and insert int sql
#   FOREACH LNKS <a>
#       link in domainList  [opt: binary in media list]
#       add page to frontier: returning ID  (call init_frontier(url))
#       add Links from page - to page (currPageId -> returning id page)