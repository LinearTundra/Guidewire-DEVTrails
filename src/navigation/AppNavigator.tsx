import React, { useEffect, useState } from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import AsyncStorage from '@react-native-async-storage/async-storage';
import OtpScreen from '../screens/OtpScreen';
import BottomTabs from './BottomTabs';

// Screens (we will create them next)
import LoginScreen from '../screens/LoginScreen';
import HomeScreen from '../screens/HomeScreen';

const Stack = createNativeStackNavigator();

export default function AppNavigator() {
  const [isLoggedIn, setIsLoggedIn] = useState<boolean | null>(null);

  useEffect(() => {
    checkLogin();
  }, []);

  const checkLogin = async () => {
    try {
      const user = await AsyncStorage.getItem('user');
      setIsLoggedIn(!!user);
    } catch (error) {
      setIsLoggedIn(false);
    }
  };

  if (isLoggedIn === null) return null;

  return (
    <NavigationContainer>
      <Stack.Navigator screenOptions={{ headerShown: false }}>
  {isLoggedIn ? (
    <Stack.Screen name="Main">
        {(props) => <BottomTabs {...props} setIsLoggedIn={setIsLoggedIn} />}
    </Stack.Screen>
  ) : (
    <>
      <Stack.Screen name="Login" component={LoginScreen} />
      <Stack.Screen name="Otp">
        {(props) => <OtpScreen {...props} setIsLoggedIn={setIsLoggedIn} />}
      </Stack.Screen>
    </>
  )}
</Stack.Navigator>
    </NavigationContainer>
  );
}