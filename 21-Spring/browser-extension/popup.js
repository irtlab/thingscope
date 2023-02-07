// Copyright 2018 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

'use strict';

chrome.storage.sync.get((result) => {
  if (result.manufacturer) {
    document.getElementById("found").innerHTML =
    `<h1 style="font-weight:normal;">ThingScope found <b>${result.manufacturer}</b> device(s)</h1>`;
  } else {
    document.getElementById("clickIt").disabled = true;
    document.getElementById("found").innerHTML =
    '<h1 style="font-weight:normal;">ThingScope did not find any devices</h1>'
  }
});


document.addEventListener('DOMContentLoaded', () => {
  let checkPageButton = document.getElementById('clickIt');
  checkPageButton.addEventListener('click', () => {
    const thingScopeURL = 'https://thingscope.cs.columbia.edu';
    chrome.tabs.create({url: thingScopeURL});
  }, false);
}, false);
