#include "lc_global.h"
#include "lc_category.h"
#include "lc_file.h"
#include "lc_profile.h"

std::vector<lcLibraryCategory> gCategories;

void lcResetDefaultCategories()
{
	lcResetCategories(gCategories);

	lcRemoveProfileKey(LC_PROFILE_CATEGORIES);
}

void lcLoadDefaultCategories(bool BuiltInLibrary)
{
	QByteArray Buffer = lcGetProfileBuffer(LC_PROFILE_CATEGORIES);

	if (Buffer.isEmpty() || !lcLoadCategories(Buffer, gCategories))
		lcResetCategories(gCategories, BuiltInLibrary);
}

void lcSaveDefaultCategories()
{
	QByteArray ByteArray;
	QTextStream Stream(&ByteArray, QIODevice::WriteOnly);

	lcSaveCategories(Stream, gCategories);

	lcSetProfileBuffer(LC_PROFILE_CATEGORIES, ByteArray);
}

void lcResetCategories(std::vector<lcLibraryCategory>& Categories, bool BuiltInLibrary)
{
	const char DefaultCategories[] =
	{
		"Wing=^%Wing\n"
	};

	const char BuiltInCategories[] =
	{
		"Brick=^%Brick\n"
	};

	QByteArray Buffer;

	if (BuiltInLibrary)
		Buffer.append(BuiltInCategories, sizeof(BuiltInCategories));
	else
		Buffer.append(DefaultCategories, sizeof(DefaultCategories));

	lcLoadCategories(Buffer, Categories);
}

bool lcLoadCategories(const QString& FileName, std::vector<lcLibraryCategory>& Categories)
{
	QFile File(FileName);

	if (!File.open(QIODevice::ReadOnly))
		return false;

	QByteArray FileData = File.readAll();

	return lcLoadCategories(FileData, Categories);
}

bool lcLoadCategories(const QByteArray& Buffer, std::vector<lcLibraryCategory>& Categories)
{
	Categories.clear();

	QTextStream Stream(Buffer);

	for (QString Line = Stream.readLine(); !Line.isNull(); Line = Stream.readLine())
	{
		int Equals = Line.indexOf('=');

		if (Equals == -1)
			continue;

		QString Name = Line.left(Equals);
		QString Keywords = Line.mid(Equals + 1);

		lcLibraryCategory Category;

		Category.Name = Name;
		Category.Keywords = Keywords.toLatin1();

		Categories.emplace_back(std::move(Category));
	}

	return true;
}

bool lcSaveCategories(const QString& FileName, const std::vector<lcLibraryCategory>& Categories)
{
	QFile File(FileName);

	if (!File.open(QIODevice::WriteOnly))
		return false;

	QTextStream Stream(&File);

	return lcSaveCategories(Stream, Categories);
}

bool lcSaveCategories(QTextStream& Stream, const std::vector<lcLibraryCategory>& Categories)
{
	QString Format("%1=%2\r\n");

	for (const lcLibraryCategory& Category : Categories)
		Stream << Format.arg(Category.Name, QString::fromLatin1(Category.Keywords));

	Stream.flush();

	return true;
}

bool lcMatchCategory(const char* PieceName, const char* Expression)
{
	// Check if we need to split the test expression.
	const char* p = Expression;

	while (*p)
	{
		if (*p == '!')
		{
			return !lcMatchCategory(PieceName, p + 1);
		}
		else if (*p == '(')
		{
//			const char* Start = p;
			int c = 0;

			// Skip what's inside the parenthesis.
			do
			{
				if (*p == '(')
						c++;
				else if (*p == ')')
						c--;
				else if (*p == 0)
					return false; // Mismatched parenthesis.

				p++;
			}
			while (c);

			if (*p == 0)
				break;
		}
		else if ((*p == '|') || (*p == '&'))
		{
			std::string LeftStr(Expression, (p - Expression) - 1);
			std::string RightStr(p + 1);

			if (*p == '|')
				return lcMatchCategory(PieceName, LeftStr.c_str()) || lcMatchCategory(PieceName, RightStr.c_str());
			else
				return lcMatchCategory(PieceName, LeftStr.c_str()) && lcMatchCategory(PieceName, RightStr.c_str());
		}

		p++;
	}

	if (strchr(Expression, '('))
	{
		p = Expression;
		while (*p)
		{
			if (*p == '(')
			{
				const char* Start = p;
				int c = 0;

				// Extract what's inside the parenthesis.
				do
				{
					if (*p == '(')
							c++;
					else if (*p == ')')
							c--;
					else if (*p == 0)
						return false; // Mismatched parenthesis.

					p++;
				}
				while (c);

				std::string SubExpression(Start + 1, p - Start - 2);
				return lcMatchCategory(PieceName, SubExpression.c_str());
			}

			p++;
		}
	}

	const char* SearchStart = Expression;
	while (isspace(*SearchStart))
		SearchStart++;

	const char* SearchEnd = SearchStart + strlen(SearchStart) - 1;
	while (SearchEnd >= SearchStart && isspace(*SearchEnd))
		SearchEnd--;

	// Testing a simple case.
	std::string Search;
	if (SearchStart != SearchEnd)
		Search = std::string(SearchStart, SearchEnd - SearchStart + 1);
	const char* Word = Search.c_str();

	// Check for modifiers.
	bool WholeWord = 0;
	bool Begin = 0;

	for (;;)
	{
		if (Word[0] == '^')
			WholeWord = true;
		else if (Word[0] == '%')
			Begin = true;
		else
			break;

		Word++;
	}

	const char* Result = strcasestr(PieceName, Word);

	if (!Result)
		return false;

	if (Begin && (Result != PieceName))
	{
		if ((Result != PieceName + 1) || ((Result[-1] != '_') && (Result[-1] != '~')))
			return false;
	}

	if (WholeWord)
	{
		char End = Result[strlen(Word)];

		if ((End != 0) && (End != ' '))
			return false;

		if ((Result != PieceName) && ((Result[-1] == '_') || (Result[-1] == '~')))
			Result--;

		if ((Result != PieceName) && (Result[-1] != ' '))
			return false;
	}

	return true;
}
