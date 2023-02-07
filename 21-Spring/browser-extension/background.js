// Copyright 2018 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

'use strict';


function stringMatching(string, value) {
  if (!value || !string) return false;

  const regex = new RegExp(value.toLowerCase(), 'g');
  const found = (string.toLowerCase()).match(regex);
  if (found) return true;
  return false;
}


function fetchDevices(callback) {
  fetch('https://thingscope.cs.columbia.edu/api/device')
    .then(r => r.json())
    .then(result => {
      callback(result);
  });
}


function main(currentURL) {
  chrome.storage.sync.set({manufacturer: ''}, () => {});
  if (currentURL) {
    fetchDevices((devices) => {
      for (let i = 0; i < devices.length; i++) {
        const manufacturer_data = devices[i].manufacturer;
        if (stringMatching(currentURL, manufacturer_data.website) ||
            stringMatching(manufacturer_data.website, currentURL)) {
          chrome.storage.sync.set({manufacturer: manufacturer_data.name}, () => {});
          return;
        }
      }
    });
  }
}


chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (/*changeInfo.status == 'complete' &&*/ tab.active) {
    main(tab.url);
  }
});
