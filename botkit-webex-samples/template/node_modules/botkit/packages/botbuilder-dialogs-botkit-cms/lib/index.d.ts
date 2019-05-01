import { TurnContext } from 'botbuilder';
import { Dialog, DialogContext, DialogInstance, DialogSet, DialogReason } from 'botbuilder-dialogs';
export interface BotkitDialogConfig {
    cms_uri: string;
    token: string;
}
export declare class BotkitHelper {
    private _config;
    private cms;
    constructor(config: BotkitDialogConfig);
    loadAllScripts(dialogSet: DialogSet): Promise<void>;
    testTriggerDC(dc: DialogContext): Promise<import("botbuilder-dialogs").DialogTurnResult<any>>;
    testTrigger(bot: any, message: any): Promise<any>;
}
export declare class BotkitDialog<O extends object = {}> extends Dialog<O> {
    script: any;
    private _config;
    private _prompt;
    private _beforeHooks;
    private _afterHooks;
    private _changeHooks;
    constructor(dialogId: string, config: BotkitDialogConfig);
    before(thread_name: any, handler: any): void;
    private runBefore;
    after(handler: (context: TurnContext, results: any) => void): void;
    private runAfter;
    onChange(variable: any, handler: any): void;
    private runOnChange;
    beginDialog(dc: any, options: any): Promise<any>;
    continueDialog(dc: any): Promise<any>;
    resumeDialog(dc: any, reason: any, result: any): Promise<any>;
    onStep(dc: any, step: any): any;
    runStep(dc: any, index: any, thread_name: any, reason: any, result?: any): any;
    endDialog(context: TurnContext, instance: DialogInstance, reason: DialogReason): Promise<void>;
    private makeOutgoing;
    private parseTemplatesRecursive;
    gotoThread(thread: any, dc: any, step: any): Promise<void>;
    private gotoThreadAction;
    private handleAction;
}
