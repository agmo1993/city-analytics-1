function (doc) {
  var source = doc.source.toLowerCase().split(/\W+/);
  if (source.includes("android")){
    emit([doc.place.bounding_box.coordinates], 1);
  }
}
