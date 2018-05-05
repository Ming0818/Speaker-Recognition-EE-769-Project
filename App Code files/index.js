import { AppRegistry } from 'react-native';
import App from './App';
import {
  StackNavigator,
  DrawerNavigator,
} from 'react-navigation'
import Audio from './screens/Audio';

import HomePage  from './screens/HomePage';
import FinalPage from './screens/FinalPage';
import AudioExample from './screens/AudioExample';

const SpeakerApp = StackNavigator({
		Home: {
			screen:HomePage
		},
		AudioPage:{
			screen :AudioExample
		},
		Model:{
			screen : Audio
		},
		FinalModel:{
			screen : FinalPage
		},
	
	},
	{ 
    	headerMode: 'none' 
  	}

);


AppRegistry.registerComponent('speaker', () => SpeakerApp);
