/**
 * Sample React Native App
 * https://github.com/facebook/react-native
 * @flow
 */

import React, { Component } from 'react';
import {AudioRecorder, AudioUtils} from 'react-native-audio';
import {
  Platform,
  StyleSheet,
  Text,
  Button,
  View
} from 'react-native';
import Toast from 'react-native-simple-toast';
import AudioExample from './screens/AudioExample';
import { NavigationActions } from 'react-navigation';
export default AudioExample;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#F5FCFF',
  },
  welcome: {
    fontSize: 20,
    textAlign: 'center',
    margin: 10,
  },
  instructions: {
    textAlign: 'center',
    color: '#333333',
    marginBottom: 5,
  },
});


