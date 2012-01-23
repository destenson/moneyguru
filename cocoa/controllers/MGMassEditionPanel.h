/* 
Copyright 2012 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "BSD" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.hardcoded.net/licenses/bsd_license
*/

#import <Cocoa/Cocoa.h>
#import "MGPanel.h"
#import "PyMassEditionPanel.h"
#import "HSComboBox.h"

@class MGMainWindowController;

@interface MGMassEditionPanel : MGPanel {
    IBOutlet NSTextField *dateField;
    IBOutlet NSTextField *descriptionField;
    IBOutlet NSTextField *payeeField;
    IBOutlet NSTextField *checknoField;
    IBOutlet NSTextField *fromField;
    IBOutlet NSTextField *toField;
    IBOutlet NSTextField *amountField;
    IBOutlet NSComboBox *currencySelector;
    IBOutlet NSButton *dateCheckBox;
    IBOutlet NSButton *descriptionCheckBox;
    IBOutlet NSButton *payeeCheckBox;
    IBOutlet NSButton *checknoCheckBox;
    IBOutlet NSButton *fromCheckBox;
    IBOutlet NSButton *toCheckBox;
    IBOutlet NSButton *amountCheckBox;
    IBOutlet NSButton *currencyCheckBox;
    
    HSComboBox *currencyComboBox;
}
- (id)initWithParent:(MGMainWindowController *)aParent;
- (PyMassEditionPanel *)model;
@end
