#include "lc_global.h"
#include "lc_qupdatedialog.h"
#include "ui_lc_qupdatedialog.h"
#include "lc_application.h"
#include "lc_library.h"
#include "lc_profile.h"
#include "lc_http.h"

void lcDoInitialUpdateCheck()
{
	int updateFrequency = lcGetProfileInt(LC_PROFILE_CHECK_UPDATES);

	if (updateFrequency == 0)
		return;

	QSettings settings;
	QDateTime CheckTime = settings.value("Updates/LastCheck", QDateTime()).toDateTime();

	if (!CheckTime.isNull())
	{
		QDateTime NextCheckTime = CheckTime.addDays(updateFrequency == 1 ? 1 : 7);

		if (NextCheckTime > QDateTime::currentDateTimeUtc())
			return;
	}

	new lcQUpdateDialog(nullptr, true);
}

lcQUpdateDialog::lcQUpdateDialog(QWidget* Parent, bool InitialUpdate)
	: QDialog(Parent), ui(new Ui::lcQUpdateDialog), mInitialUpdate(InitialUpdate)
{
	ui->setupUi(this);

	connect(this, SIGNAL(finished(int)), this, SLOT(finished(int)));

	ui->status->setText(tr("Connecting to update server..."));

	mHttpManager = new lcHttpManager(this);
	connect(mHttpManager, SIGNAL(DownloadFinished(lcHttpReply*)), this, SLOT(DownloadFinished(lcHttpReply*)));

	mHttpManager->DownloadFile(QLatin1String("https://www.SECAD.org/updates.txt"));
}

lcQUpdateDialog::~lcQUpdateDialog()
{
	delete ui;
}

void lcQUpdateDialog::accept()
{
	QSettings settings;
	settings.setValue("Updates/IgnoreVersion", versionData);

	QDialog::accept();
}

void lcQUpdateDialog::reject()
{
	QDialog::reject();
}

void lcQUpdateDialog::finished(int result)
{
	Q_UNUSED(result);

	if (mInitialUpdate)
		deleteLater();
}

void lcQUpdateDialog::DownloadFinished(lcHttpReply *reply)
{
	bool updateAvailable = false;

	if (reply->error() == QNetworkReply::NoError)
	{
		int majorVersion, minorVersion, patchVersion;
		int parts;

		versionData = reply->readAll();
		const char *update = versionData;

		QSettings settings;
		QByteArray ignoreUpdate = settings.value("Updates/IgnoreVersion", QByteArray()).toByteArray();

		if (mInitialUpdate && ignoreUpdate == versionData)
		{
			updateAvailable = false;
		}
		else if (sscanf(update, "%d.%d.%d %d", &majorVersion, &minorVersion, &patchVersion, &parts) == 4)
		{
			QString status;

			if (majorVersion > LC_VERSION_MAJOR)
				updateAvailable = true;
			else if (majorVersion == LC_VERSION_MAJOR)
			{
				if (minorVersion > LC_VERSION_MINOR)
					updateAvailable = true;
				else if (minorVersion == LC_VERSION_MINOR)
				{
					if (patchVersion > LC_VERSION_PATCH)
						updateAvailable = true;
				}
			}

			if (updateAvailable)
				status = QString(tr("<p>There's a newer version of SECAD available for download (%1.%2.%3).</p>")).arg(QString::number(majorVersion), QString::number(minorVersion), QString::number(patchVersion));
			else
				status = tr("<p>You are using the latest SECAD version.</p>");

			lcPiecesLibrary* library = lcGetPiecesLibrary();

			if (library->mNumOfficialPieces)
			{
				if (parts > library->mNumOfficialPieces)
				{
					status += tr("<p>There are new parts available.</p>");
					updateAvailable = true;
				}
				else
					status += tr("<p>There are no new parts available at this time.</p>");
			}

			if (updateAvailable)
			{
				status += tr("<p>Visit <a href=\"https://github.com/leozide/SECAD/releases\">https://github.com/leozide/SECAD/releases</a> to download.</p>");
			}

			ui->status->setText(status);
		}
		else
			ui->status->setText(tr("Error parsing update information."));

		settings.setValue("Updates/LastCheck", QDateTime::currentDateTimeUtc());
	}
	else
		ui->status->setText(tr("Error connecting to the update server."));

	if (mInitialUpdate)
	{
		if (updateAvailable)
			show();
		else
			deleteLater();
	}

	if (updateAvailable)
		ui->buttonBox->setStandardButtons(QDialogButtonBox::Close | QDialogButtonBox::Ignore);
	else
		ui->buttonBox->setStandardButtons(QDialogButtonBox::Close);
}
