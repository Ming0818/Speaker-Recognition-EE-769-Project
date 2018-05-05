import React, {Component} from 'react';

import {
  AppRegistry,
  StyleSheet,
  Text,
  View,
  TouchableHighlight,
  Platform,
  PermissionsAndroid,
} from 'react-native';
import Toast from 'react-native-simple-toast';
import Sound from 'react-native-sound';
import {AudioRecorder, AudioUtils} from 'react-native-audio';
import { NavigationActions } from 'react-navigation';

class Audio extends Component {

    state = {
      currentTime: 0.0,
      recording: false,
      paused: false,
      stoppedRecording: false,
      finished: false ,
      count:0,
      audioPath: AudioUtils.DocumentDirectoryPath ,
      hasPermission: undefined,
    };

    prepareRecordingPath(audioPath){
      AudioRecorder.prepareRecordingAtPath(audioPath, {
        SampleRate: 22050,
        Channels: 1,
        AudioQuality: "Low",
        AudioEncoding: "flac",
        AudioEncodingBitRate: 32000
      });
    }

    componentDidMount() {
      this._checkPermission().then((hasPermission) => {
        this.setState({ hasPermission });

        if (!hasPermission) return;
        var count_str = ''+this.state.count;
        this.prepareRecordingPath(this.state.audioPath + '/test'+count_str+'.flac');

        AudioRecorder.onProgress = (data) => {
          this.setState({currentTime: Math.floor(data.currentTime)});
        };

        AudioRecorder.onFinished = (data) => {
          // Android callback comes in the form of a promise instead.
          if (Platform.OS === 'ios') {
            this._finishRecording(data.status === "OK", data.audioFileURL);
          }
        };
      });
    }

    _checkPermission() {
      if (Platform.OS !== 'android') {
        return Promise.resolve(true);
      }

      const rationale = {
        'title': 'Microphone Permission',
        'message': 'AudioExample needs access to your microphone so you can record audio.'
      };

      return PermissionsAndroid.request(PermissionsAndroid.PERMISSIONS.RECORD_AUDIO, rationale)
        .then((result) => {
          console.log('Permission result:', result);
          return (result === true || result === PermissionsAndroid.RESULTS.GRANTED);
        });
    }

    _renderButton(title, onPress, active) {
      var style = (active) ? styles.activeButtonText : styles.buttonText;

      return (
        <TouchableHighlight style={styles.submit} onPress={onPress}>
          <Text style={style}>
            {title}
          </Text>
        </TouchableHighlight>
      );
    }

    _renderPauseButton(onPress, active) {
      var style = (active) ? styles.activeButtonText : styles.buttonText;
      var title = this.state.paused ? "RESUME" : "PAUSE";
      return (
        <TouchableHighlight style={styles.button} onPress={onPress}>
          <Text style={style}>
            {title}
          </Text>
        </TouchableHighlight>
      );
    }

    async _pause() {
      if (!this.state.recording) {
        console.warn('Can\'t pause, not recording!');
        return;
      }

      try {
        const filePath = await AudioRecorder.pauseRecording();
        this.setState({paused: true});
      } catch (error) {
        console.error(error);
      }
    }

    async _resume() {
      if (!this.state.paused) {
        console.warn('Can\'t resume, not paused!');
        return;
      }

      try {
        await AudioRecorder.resumeRecording();
        this.setState({paused: false});
      } catch (error) {
        console.error(error);
      }
    }

    async _stop() {
      if (!this.state.recording) {
        console.warn('Can\'t stop, not recording!');
        return;
      }

      this.setState({stoppedRecording: true, recording: false, paused: false});

      try {
        const filePath = await AudioRecorder.stopRecording();

        if (Platform.OS === 'android') {
          this._finishRecording(true, filePath);
        }
        return filePath;
      } catch (error) {
        console.error(error);
      }
    }

    async _play() {
      // console.log(this.state.audioPath);
      // Toast.show(this.state.audioPath, Toast.LONG);
      if (this.state.recording) {
        await this._stop();
      }
      // this.uploadAudio
      // These timeouts are a hacky workaround for some issues with react-native-sound.
      // See https://github.com/zmxv/react-native-sound/issues/89.
      setTimeout(() => {
        var t = this.state.count -1;
      var count_str = ''+t;
        var sound = new Sound(this.state.audioPath  + '/test'+count_str+'.flac' , '', (error) => {
          if (error) {
            console.log('failed to load the sound', error);
          }
        });

        setTimeout(() => {
          sound.play((success) => {
            if (success) {
              console.log('successfully finished playing');
            } else {
              console.log('playback failed due to audio decoding errors');
            }
          });
        }, 100);
      }, 100);
    }
    async uploadAudio() {
      var url = "http://192.168.0.106:8000/makeModel/";
      var type = this.props.navigation.state.params.type;
      var name = this.props.navigation.state.params.name
      var c = this.state.count;
      const formData = new FormData()
      formData.append('name',name);
      for (var j=0;j < c;j++){
        var count_str = ''+j;
        const path = 'file://' + this.state.audioPath  + '/test'+count_str+'.flac'
        formData.append('file'+count_str, {
          uri: path,
          name: 'test.flac',
          type: 'audio/flac',
        })
      }
      
      fetch(url,{
          method: "POST",
          body: formData
        })
        .then((response) => response.json())
        .then((responseData) => {
          // Toast.show(responseData['status'],Toast.SHORT)
          // Toast.show(responseData['data'],Toast.SHORT)
          this.props.navigation.navigate('FinalModel',{final:'Welcome '+name +' Your Data is recorded'});
        })
        .catch( (error) => {
          console.log(error);
          Toast.show("Error Fetching ", Toast.SHORT);
        })
        .done();
    }
    async _record() {
      if (this.state.recording) {
        console.warn('Already recording!');
        return;
      }

      if (!this.state.hasPermission) {
        console.warn('Can\'t record, no permission granted!');
        return;
      }

      if(this.state.stoppedRecording){
        var count_str = ''+this.state.count;
        this.prepareRecordingPath(this.state.audioPath + '/test'+count_str+'.flac');
      }

      this.setState({recording: true, paused: false});

      try {
        const filePath = await AudioRecorder.startRecording();
      } catch (error) {
        console.error(error);
      }
    }

    _finishRecording(didSucceed, filePath) {
      this.setState({ finished: didSucceed });
      var c = this.state.count;
      c = c+1;
      this.setState({count: c});
      console.log(`Finished recording of duration ${this.state.currentTime} seconds at path: ${filePath}`);
    }

    render() {
      var type = this.props.navigation.state.params.type
      return (
        <View style={styles.content}>
          <Text style={styles.welcome}>Speaker {type}</Text>
          <View style={styles.controls}>
            {this._renderButton("RECORD", () => {this._record()}, this.state.recording )}
            {this._renderButton("PLAY", () => {this._play()} )}
            {this._renderButton("STOP", () => {this._stop()} )}
            {this._renderButton("UPLOAD", () => {this.uploadAudio()} )}
            <Text style={styles.activeButtonText}>{this.state.count} sample recorded</Text>
            {/* {this._renderButton("PAUSE", () => {this._pause()} )} */}
            <Text style={styles.progressText}>{this.state.currentTime}s</Text>
          </View>
        </View>
      );
    }
  }

  var styles = StyleSheet.create({
    container: {
      flex: 1,
      backgroundColor: "#fff",
    },
    controls: {
      justifyContent: 'center',
      alignItems: 'center',
      flex: 1,
    },
     welcome: {
    fontSize: 20,
    color: '#2e2f30',
    textAlign: 'center',
    // marginTop: 10,
    // marginBottom: 10,
    backgroundColor: '#fff',
    padding: 20
  },
    content:{
      flex:1,
  },
    progressText: {
      paddingTop: 50,
      fontSize: 50,
      color: "#0c3270"
    },
    button: {
      padding: 20
    },
    disabledButtonText: {
      color: '#eee'
    },
    buttonText: {
      fontSize: 20,
      color: "#f4f5f7"
    },
    submit: {
      margin: 20 ,
        alignSelf:'center',
        padding: 10,
        backgroundColor: '#4c83db',
      borderWidth: 1,
      borderRadius: 10,
        width: 250 
    },
    activeButtonText: {
      fontSize: 20,
      color: "#B81F00"
    }

  });

export default Audio;