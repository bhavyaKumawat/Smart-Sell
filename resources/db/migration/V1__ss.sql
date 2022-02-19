
CREATE TABLE [dbo].[SmartSellLogs](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[TransactionId] [uniqueidentifier] NULL,
	[CreatedBy] [nvarchar](350) NULL,
	[CreatedOn] [datetime] NULL,
	[OrderId] [nvarchar](200) NOT NULL,
	[SmartSellItemId] [nvarchar](1048) NULL,
	[SmartSellGroupId] [nvarchar](1048) NULL,
	[SmartSellLinkedItemId] [nvarchar](1048) NULL,
	[SmartSellDeclined] [bit] NULL,
	[SmartSellAmount] [decimal](10, 8) NULL,
	[RuleID] [int] NULL,
	[CrewSmartSellTimeInMs] [bigint] NULL,
	[EmployeeId] [nvarchar](100) NULL,
	[EmployeeName] [nvarchar](200) NULL,
	[TerminalId] [nvarchar](350) NULL,
	[TerminalName] [nvarchar](350) NULL,
	[LocationId] [uniqueidentifier] NULL,
	[StoreId] [nvarchar](350) NULL,
	[TransactionDateTime] [datetime] NULL,
	[RowCreatedOn] [datetime] NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[SmartSellStatusLogs]    Script Date: 2/16/2022 10:51:18 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[SmartSellStatusLogs](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[CreatedBy] [nvarchar](700) NULL,
	[CreatedOn] [datetime] NULL,
	[SmartSellStatus] [bit] NULL,
	[TransactionDateTime] [datetime] NULL,
	[LocationId] [uniqueidentifier] NULL,
	[TerminalId] [nvarchar](350) NULL,
	[TerminalName] [nvarchar](350) NULL,
	[StoreId] [nvarchar](350) NULL,
	[Timezone] [nvarchar](700) NULL
) ON [PRIMARY]
GO
ALTER TABLE [dbo].[SmartSellLogs] ADD  CONSTRAINT [DF_SmartSell_RowCreated]  DEFAULT (getutcdate()) FOR [RowCreatedOn]
GO
ALTER TABLE [dbo].[SmartSellStatusLogs] ADD  DEFAULT (getutcdate()) FOR [CreatedOn]
GO