function (doc) {
  var source = doc.source.toLowerCase().split(/\W+/);
  if (source.includes("iphone")){
    emit([doc.place.bounding_box.coordinates], 1);
  }
}
