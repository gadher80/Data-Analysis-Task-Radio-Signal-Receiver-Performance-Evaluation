"""
Author : Hardik Gadher
Code: Coding Challenge for Jon Interview
Content: Solution for matching detected vehicle records
Date: 08.04.2022
Location: Erfurt, Germany
"""

# ======================================================================================================================================

import json
import pandas as pd
from datetime import datetime
from math import radians,cos,sin,asin,sqrt
import matplotlib.pyplot as plt


class Match :
    """
    Solution to combine detected data
    """

    def __init__(self,receiverAddress,vehicleAddress) :

        """
        :param receiverAddress: file path for receiver data file
        :param vehicleAddress: file path for vehicle data file
        :type receiverAddress: String,
        :type  vehicleAddress : String
        """

        self.longitude_receiver = None
        self.lattitude_receiver = None
        self.df_Vehicle = None
        self.receiverAddress = receiverAddress
        self.vehicleAddress = vehicleAddress

    def recordMatch(self) :

        """
        :return: Combined datasets (csv format), and kept only those data where the receiver detected the vehicle
        :Note : In this method Question 1 and 2 & are answered
        """

        ReceviverJson = open(self.receiverAddress)
        data = json.load(ReceviverJson)

        # extract list from Json data
        Timestamp = [datetime.fromtimestamp(record['Timestamp']) for record in data]
        Strength = [record['Signal Strength'] for record in data]

        # create dataframe for receiver data
        df_Receiver = pd.DataFrame(Timestamp,columns=['Timestamp'])
        df_Receiver['Timestamp'] = Timestamp

        # create dataframe for vehicle data & grab rows where 'Status_POS_Heading_deg' is 1
        self.df_Vehicle = pd.read_csv(self.vehicleAddress)
        self.df_Vehicle = self.df_Vehicle[(self.df_Vehicle['Status_POS_Heading_deg'] != 0)]

        # create datetime column to compare receiver datetime records
        self.df_Vehicle['DateTime'] = pd.to_datetime(self.df_Vehicle['Date_UTC']) + pd.to_timedelta(
            self.df_Vehicle['Time_UTC'])
        self.df_Vehicle['Strength'] = ''

        # set similar datatype for both time stamps from both dataframe
        DatetimeList = [date.to_pydatetime() for date in self.df_Vehicle['DateTime'].tolist()]
        TimestampList = [time.to_pydatetime() for time in df_Receiver['Timestamp'].tolist()]

        # find a match where maximum allowed time difference for a match TimeDifference = 100 ms
        # store them in a list called DetectedRecord
        ReceiverDict = dict(zip(TimestampList,Strength))
        StregthList = []
        DetectedRecord = []
        for record,strength in ReceiverDict.items() :
            for recordTime in DatetimeList :
                Logtime = record - recordTime
                if 0 <= Logtime.total_seconds() * 1000 < 100 :
                    DetectedRecord.append(recordTime)
                    StregthList.append(strength)

        # drop other rows and keep only matched records
        Index_List = []
        for value in DetectedRecord :
            for index_vehicle,match_vehicle in self.df_Vehicle['DateTime'].iteritems() :
                if value == self.df_Vehicle.loc[index_vehicle,'DateTime'] :
                    Index_List.append(index_vehicle)
                    break

        self.df_Vehicle = self.df_Vehicle.loc[Index_List,:]
        self.df_Vehicle['Strength'] = pd.Series(StregthList).values
        self.df_Vehicle.drop('DateTime',inplace=True,axis=1)
        return self.df_Vehicle.to_csv('output.csv')

    def vehicleDistance(self,longitude_receiver,lattitude_receiver) :

        """
        :param longitude_receiver: Given in question
        :param lattitude_receiver: GIven in question
        :return: distance between the receiver and the vehicle in km for each match.
        :type longitude_receiver: float,
        :type lattitude_receiver : float
        :note : In this method Question 3 is answered
        """

        self.longitude_receiver = longitude_receiver
        self.lattitude_receiver = lattitude_receiver

        # set to similar datatypes from different datatypes
        self.df_Vehicle['POS_Longitude_WGS84_deg'] = self.df_Vehicle['POS_Longitude_WGS84_deg'].astype(float)
        self.df_Vehicle['POS_Latitude_WGS84_deg'] = self.df_Vehicle['POS_Latitude_WGS84_deg'].astype(float)
        POS_Longitude_WGS84_degList = self.df_Vehicle['POS_Longitude_WGS84_deg'].tolist()
        POS_Latitude_WGS84_degList = self.df_Vehicle['POS_Latitude_WGS84_deg'].tolist()

        self.df_Vehicle['Distance'] = ''
        self.df_Vehicle.reset_index(inplace=True,drop=True)
        r = 6371

        DistanceList = []
        Cordinates = [(POS_Longitude_WGS84_degList[a],POS_Latitude_WGS84_degList[a]) for a in
                      range(len(POS_Longitude_WGS84_degList))]

        # calculate distance using 2 cordinates' values
        for cordinate in Cordinates :
            longitude_emmiter = radians(cordinate[0])
            lattitude_emmiter = radians(cordinate[1])
            dlon = radians(self.longitude_receiver) - longitude_emmiter
            dlat = radians(self.lattitude_receiver) - lattitude_emmiter
            D_Distance = sin(dlat / 2) ** 2 + cos(lattitude_emmiter) * cos(radians(self.lattitude_receiver)) * sin(
                dlon / 2) ** 2
            c = 2 * asin(sqrt(D_Distance))
            DistanceList.append(c * r)

        self.df_Vehicle['Distance'] = pd.Series(DistanceList)
        return self.df_Vehicle.to_csv('Light_Out.csv')

    def distancePlot(self) :

        """
        :return: plot showing the signal strength vs. distance to receiver.
        :Note : In this method Question 4 is answered.
        """

        self.df_Vehicle.plot(x='Strength',y='Distance',style='o')
        return plt.savefig("DistanceScatter.png",bbox_inches='tight',dpi=300)


# calling objects

if __name__ == '__main__' :
    recordObject = Match('receiver.json','vehicle.csv')
    recordObject.recordMatch()
    recordObject.vehicleDistance(9.45778,53.972401)
    recordObject.distancePlot()

# ======================================================================================================================================
