import React from 'react';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { Ionicons } from '@expo/vector-icons';

import HomeScreen from '../screens/HomeScreen';
import PoliciesScreen from '../screens/PoliciesScreen';
import ClaimsScreen from '../screens/ClaimsScreen';
import ProfileScreen from '../screens/ProfileScreen';

const Tab = createBottomTabNavigator();

export default function BottomTabs({ setIsLoggedIn }: any) {
  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        headerShown: false,
        tabBarStyle: { backgroundColor: '#0B0F1A', borderTopWidth: 0 },
        tabBarActiveTintColor: '#4CAF50',
        tabBarInactiveTintColor: '#aaa',
        tabBarIcon: ({ color, size }) => {
          let iconName: any;

          if (route.name === 'Home') iconName = 'home';
          else if (route.name === 'Policies') iconName = 'document-text';
          else if (route.name === 'Claims') iconName = 'cash';
          else if (route.name === 'Profile') iconName = 'person';

          return <Ionicons name={iconName} size={size} color={color} />;
        },
      })}
    >
      {/* Home */}
      <Tab.Screen name="Home">
        {(props) => <HomeScreen {...props} setIsLoggedIn={setIsLoggedIn} />}
      </Tab.Screen>

      {/* Policies */}
      <Tab.Screen name="Policies" component={PoliciesScreen} />

      {/* Claims */}
      <Tab.Screen name="Claims" component={ClaimsScreen} />

      {/* Profile */}
      <Tab.Screen name="Profile" component={ProfileScreen} />
    </Tab.Navigator>
  );
}