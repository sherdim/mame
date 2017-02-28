function coapp(){document.title+=" - PYLAB";};
coapp();
events.on("notebook_loaded.Notebook", function () {coapp()});
events.on('notebook_saved.Notebook', function () {coapp()});
events.on('notebook_renamed.Notebook', function () {coapp()});

